//! Real-time 3D view of the cube: plays the scramble from a solved cube, then
//! the solution, animating every face turn.

use std::f32::consts::FRAC_PI_2;

use macroquad::prelude::*;

use rubik::geometry::dot;
use rubik::{Cube, Move};

const BACKGROUND: Color = Color::new(0.11, 0.12, 0.15, 1.0);
const BODY: Color = Color::new(0.06, 0.06, 0.07, 1.0);
const DIM: Color = Color::new(0.45, 0.47, 0.52, 1.0);
const HIGHLIGHT: Color = Color::new(1.0, 0.8, 0.2, 1.0);

/// Half the size of a cubie body. Cubies are 1 apart, leaving a thin gap.
const BODY_HALF: f32 = 0.49;
/// Half the size of a sticker.
const STICKER_HALF: f32 = 0.42;
/// How far stickers float above the body, to avoid z-fighting.
const STICKER_LIFT: f32 = 0.01;

const MIN_SPEED: f32 = 0.25;
const MAX_SPEED: f32 = 30.0;
/// Time to wait between the end of the scramble and the start of the solve.
const PHASE_PAUSE: f32 = 1.0;

fn paint(color: rubik::Color) -> Color {
    let [r, g, b] = match color {
        rubik::Color::White => [240, 240, 240],
        rubik::Color::Yellow => [255, 213, 0],
        rubik::Color::Red => [196, 30, 58],
        rubik::Color::Green => [0, 158, 96],
        rubik::Color::Blue => [0, 81, 186],
        rubik::Color::Orange => [255, 88, 0],
    };
    Color::from_rgba(r, g, b, 255)
}

fn to_vec3(v: [i32; 3]) -> Vec3 {
    vec3(v[0] as f32, v[1] as f32, v[2] as f32)
}

/// Opens a window showing `scramble` then `solution` being played.
pub fn run(scramble: Vec<Move>, solution: Vec<Move>) {
    let conf = Conf {
        window_title: "rubik".to_owned(),
        window_width: 1000,
        window_height: 750,
        high_dpi: true,
        sample_count: 4,
        ..Default::default()
    };
    macroquad::Window::from_config(conf, Player::new(scramble, solution).run());
}

/// A face turn being animated.
struct Turn {
    /// The move actually performed (the inverse one when stepping back).
    m: Move,
    backward: bool,
    /// From 0 to 1.
    progress: f32,
}

impl Turn {
    /// Rotation of the turned layer at the current point of the animation.
    fn rotation(&self) -> Quat {
        // `Move::matrix` turns clockwise, which is a negative angle around the
        // face normal. `X'` is animated as a quarter turn the other way.
        let quarters = match self.m.turns {
            1 => -1.0,
            2 => -2.0,
            _ => 1.0,
        };
        let t = self.progress;
        let eased = t * t * (3.0 - 2.0 * t);
        Quat::from_axis_angle(to_vec3(self.m.face.normal()), quarters * FRAC_PI_2 * eased)
    }

    fn duration(&self, speed: f32) -> f32 {
        let quarters = if self.m.turns == 2 { 1.5 } else { 1.0 };
        quarters / speed
    }
}

/// Camera turning around the cube.
struct Orbit {
    yaw: f32,
    pitch: f32,
    distance: f32,
}

impl Orbit {
    fn eye(&self) -> Vec3 {
        let (sin_yaw, cos_yaw) = self.yaw.sin_cos();
        let (sin_pitch, cos_pitch) = self.pitch.sin_cos();
        self.distance * vec3(cos_pitch * sin_yaw, sin_pitch, cos_pitch * cos_yaw)
    }

    fn camera(&self) -> Camera3D {
        Camera3D {
            position: self.eye(),
            target: Vec3::ZERO,
            up: Vec3::Y,
            ..Default::default()
        }
    }
}

struct Player {
    /// The scramble followed by the solution.
    moves: Vec<Move>,
    scramble_len: usize,
    /// Number of moves of `moves` already applied to `cube`.
    done: usize,
    cube: Cube,
    turn: Option<Turn>,
    playing: bool,
    /// Quarter turns per second.
    speed: f32,
    /// Seconds to wait before starting the next move.
    wait: f32,
    orbit: Orbit,
    last_mouse: Vec2,
}

impl Player {
    fn new(scramble: Vec<Move>, solution: Vec<Move>) -> Player {
        let scramble_len = scramble.len();
        Player {
            moves: scramble.into_iter().chain(solution).collect(),
            scramble_len,
            done: 0,
            cube: Cube::new(),
            turn: None,
            playing: true,
            speed: 3.0,
            wait: 0.5,
            orbit: Orbit {
                yaw: 0.6,
                pitch: 0.5,
                distance: 9.0,
            },
            last_mouse: Vec2::ZERO,
        }
    }

    async fn run(mut self) {
        loop {
            if is_key_pressed(KeyCode::Escape) || is_key_pressed(KeyCode::Q) {
                break;
            }
            self.handle_input();
            self.update(get_frame_time());

            clear_background(BACKGROUND);
            set_camera(&self.orbit.camera());
            draw_mesh(&self.mesh());
            set_default_camera();
            self.draw_hud();

            next_frame().await;
        }
    }

    fn finished(&self) -> bool {
        self.done == self.moves.len()
    }

    fn restart(&mut self) {
        self.cube = Cube::new();
        self.done = 0;
        self.turn = None;
        self.wait = 0.0;
    }

    fn start_forward(&mut self) {
        self.turn = Some(Turn {
            m: self.moves[self.done],
            backward: false,
            progress: 0.0,
        });
    }

    fn start_backward(&mut self) {
        self.turn = Some(Turn {
            m: self.moves[self.done - 1].inverse(),
            backward: true,
            progress: 0.0,
        });
    }

    fn handle_input(&mut self) {
        if is_key_pressed(KeyCode::Space) {
            if self.finished() && self.turn.is_none() {
                self.restart();
                self.playing = true;
            } else {
                self.playing = !self.playing;
            }
        }
        if is_key_pressed(KeyCode::Right) && self.turn.is_none() && !self.finished() {
            self.playing = false;
            self.start_forward();
        }
        if is_key_pressed(KeyCode::Left) && self.turn.is_none() && self.done > 0 {
            self.playing = false;
            self.start_backward();
        }
        if is_key_pressed(KeyCode::Up) {
            self.speed = (self.speed * 1.5).min(MAX_SPEED);
        }
        if is_key_pressed(KeyCode::Down) {
            self.speed = (self.speed / 1.5).max(MIN_SPEED);
        }
        if is_key_pressed(KeyCode::R) {
            self.restart();
            self.playing = false;
        }
        if is_key_pressed(KeyCode::S) && self.done < self.scramble_len {
            self.turn = None;
            self.cube
                .apply_all(&self.moves[self.done..self.scramble_len]);
            self.done = self.scramble_len;
            self.wait = PHASE_PAUSE;
        }

        let mouse = Vec2::from(mouse_position());
        if is_mouse_button_down(MouseButton::Left) {
            let delta = mouse - self.last_mouse;
            self.orbit.yaw -= delta.x * 0.01;
            self.orbit.pitch = (self.orbit.pitch + delta.y * 0.01).clamp(-1.5, 1.5);
        }
        self.last_mouse = mouse;

        let (_, wheel) = mouse_wheel();
        if wheel != 0.0 {
            let factor = if wheel > 0.0 { 0.9 } else { 1.0 / 0.9 };
            self.orbit.distance = (self.orbit.distance * factor).clamp(5.0, 25.0);
        }
    }

    fn update(&mut self, dt: f32) {
        if let Some(turn) = &mut self.turn {
            turn.progress += dt / turn.duration(self.speed);
            if turn.progress >= 1.0 {
                self.cube.apply(turn.m);
                if turn.backward {
                    self.done -= 1;
                } else {
                    self.done += 1;
                    if self.done == self.scramble_len {
                        self.wait = PHASE_PAUSE;
                    }
                }
                self.turn = None;
            }
        } else if self.playing {
            if self.wait > 0.0 {
                self.wait -= dt;
            } else if self.finished() {
                self.playing = false;
            } else {
                self.start_forward();
            }
        }
    }

    /// Cubie bodies and stickers, with the turning layer rotated.
    fn mesh(&self) -> Mesh {
        let mut mesh = Mesh {
            vertices: Vec::with_capacity(26 * 24 + 54 * 4),
            indices: Vec::with_capacity(26 * 36 + 54 * 6),
            texture: None,
        };
        let eye = self.orbit.eye().normalize();
        let rotation_of = |position: [i32; 3]| match &self.turn {
            Some(turn) if dot(position, turn.m.face.normal()) == 1 => turn.rotation(),
            _ => Quat::IDENTITY,
        };

        for x in -1..=1 {
            for y in -1..=1 {
                for z in -1..=1 {
                    let position = [x, y, z];
                    if position == [0, 0, 0] {
                        continue;
                    }
                    let rotation = rotation_of(position);
                    for normal in [
                        Vec3::X,
                        Vec3::NEG_X,
                        Vec3::Y,
                        Vec3::NEG_Y,
                        Vec3::Z,
                        Vec3::NEG_Z,
                    ] {
                        let center = to_vec3(position) + normal * BODY_HALF;
                        push_quad(&mut mesh, center, normal, BODY_HALF, rotation, BODY, eye);
                    }
                }
            }
        }

        for (sticker, color) in self.cube.stickers() {
            let normal = to_vec3(sticker.normal);
            let center = to_vec3(sticker.position) + normal * (0.5 + STICKER_LIFT);
            let rotation = rotation_of(sticker.position);
            push_quad(
                &mut mesh,
                center,
                normal,
                STICKER_HALF,
                rotation,
                paint(color),
                eye,
            );
        }
        mesh
    }

    fn draw_hud(&self) {
        let margin = 20.0;
        let solving = self.done > self.scramble_len
            || (self.done == self.scramble_len && self.turn.as_ref().is_none_or(|t| !t.backward));
        let (phase, start, end) = if solving {
            ("Solve", self.scramble_len, self.moves.len())
        } else {
            ("Scramble", 0, self.scramble_len)
        };

        let status = if self.finished() && self.turn.is_none() {
            "Solved!".to_owned()
        } else {
            let state = if self.playing { "playing" } else { "paused" };
            format!("{phase} {}/{}  ({state})", self.done - start, end - start)
        };
        draw_text(&status, margin, margin + 18.0, 32.0, WHITE);
        draw_text(
            format!("speed {:.2} turns/s", self.speed),
            margin,
            margin + 44.0,
            20.0,
            DIM,
        );

        // The moves of the current phase, wrapped, with the current one highlighted.
        let current = match &self.turn {
            Some(turn) if turn.backward => self.done - 1,
            _ => self.done,
        };
        let font_size = 24.0;
        let space = measure_text(" ", None, font_size as u16, 1.0).width;
        let (mut x, mut y) = (margin, margin + 80.0);
        for i in start..end {
            let text = self.moves[i].to_string();
            let width = measure_text(&text, None, font_size as u16, 1.0).width;
            if x + width > screen_width() - margin {
                x = margin;
                y += font_size;
            }
            let color = if i == current {
                HIGHLIGHT
            } else if i < self.done {
                DIM
            } else {
                WHITE
            };
            draw_text(&text, x, y, font_size, color);
            x += width + space * 1.5;
        }

        draw_text(
            "Space play/pause   Left/Right step   Up/Down speed   S skip scramble   \
             R restart   drag rotate   scroll zoom   Esc quit",
            margin,
            screen_height() - margin,
            18.0,
            DIM,
        );
    }
}

/// Adds a square of half size `half` centered on `center` and facing `normal`,
/// rotated around the origin by `rotation`. It is shaded by how much it faces
/// the camera, which sits in direction `eye`.
fn push_quad(
    mesh: &mut Mesh,
    center: Vec3,
    normal: Vec3,
    half: f32,
    rotation: Quat,
    color: Color,
    eye: Vec3,
) {
    let u = if normal.x.abs() > 0.5 {
        Vec3::Y
    } else {
        Vec3::X
    } * half;
    let v = normal.cross(u);
    let light = 0.55 + 0.45 * (rotation * normal).dot(eye).max(0.0);
    let shaded = Color::new(color.r * light, color.g * light, color.b * light, color.a);

    let base = mesh.vertices.len() as u16;
    for corner in [
        center - u - v,
        center + u - v,
        center + u + v,
        center - u + v,
    ] {
        mesh.vertices
            .push(Vertex::new2(rotation * corner, Vec2::ZERO, shaded));
    }
    mesh.indices.extend([0, 1, 2, 0, 2, 3].map(|i| base + i));
}
