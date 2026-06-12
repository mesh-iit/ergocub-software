import argparse
from pathlib import Path
import time
import xml.etree.ElementTree as ET

import mujoco
import mujoco.viewer
import resolve_robotics_uri_py as rru

from mujoco_urdf_loader import (
    CameraCfg,
    ControlMode,
    GyroSensorCfg,
    URDFtoMuJoCoLoader,
    URDFtoMuJoCoLoaderCfg,
)
from mujoco_urdf_loader.urdf_fcn import get_mesh_path


DEFAULT_ROBOT_MODEL = "ergoCubSN001"
DEFAULT_OUTPUT = "ergocub.xml"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a MuJoCo XML model from an ergoCub URDF."
    )
    parser.add_argument(
        "--robot-model",
        default=DEFAULT_ROBOT_MODEL,
        help=(
            "Robot model name under package://ergoCub/robots, a package URI, "
            "or a local URDF path."
        ),
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Path where the generated MJCF XML file is written.",
    )
    parser.add_argument(
        "--contact-forces",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Show contact-force visualizations in the MuJoCo viewer.",
    )
    return parser.parse_args()


def resolve_robot_model(robot_model):
    robot_model = robot_model.strip()
    robot_model_path = Path(robot_model).expanduser()

    if "://" in robot_model:
        return str(rru.resolve_robotics_uri(robot_model))

    if robot_model_path.exists() or robot_model_path.suffix == ".urdf":
        return str(robot_model_path)

    if robot_model.startswith("SN"):
        robot_model = f"ergoCub{robot_model}"

    return str(
        rru.resolve_robotics_uri(
            f"package://ergoCub/robots/{robot_model}/model.urdf"
        )
    )


args = parse_args()

observed_joints = [
    "l_hip_pitch",
    "r_hip_pitch",
    "torso_roll",
    "l_hip_roll",
    "r_hip_roll",
    "torso_pitch",
    "torso_yaw",
    "l_hip_yaw",
    "r_hip_yaw",
    "l_shoulder_pitch",
    "neck_pitch",
    "r_shoulder_pitch",
    "l_knee",
    "r_knee",
    "l_shoulder_roll",
    "neck_roll",
    "r_shoulder_roll",
    "l_ankle_pitch",
    "r_ankle_pitch",
    "neck_yaw",
    "camera_tilt",
    "l_ankle_roll",
    "r_ankle_roll",
    "l_shoulder_yaw",
    "r_shoulder_yaw",
    "l_elbow",
    "r_elbow",
]

actuated_joints = observed_joints

control_modes = [ControlMode.POSITION] * len(observed_joints)
stiffness = [1000.0] * len(observed_joints)
damping = [2.0] * len(observed_joints)

gyro_sensors_cfg = [
    GyroSensorCfg(site="realsense_depth_frame", name="realsense_depth_gyro"),
    GyroSensorCfg(site="realsense_rgb_frame", name="realsense_rgb_gyro"),
    GyroSensorCfg(site="head_imu_0", name="head_gyro"),
    GyroSensorCfg(site="waist_imu_0", name="torso_gyro"),
    GyroSensorCfg(site="l_arm_ft", name="l_arm_gyro"),
    GyroSensorCfg(site="r_arm_ft", name="r_arm_gyro"),
    GyroSensorCfg(site="l_leg_ft", name="l_hip_gyro"),
    GyroSensorCfg(site="r_leg_ft", name="r_hip_gyro"),
    GyroSensorCfg(site="l_foot_front_ft", name="l_foot_front_gyro"),
    GyroSensorCfg(site="l_foot_rear_ft", name="l_foot_rear_gyro"),
    GyroSensorCfg(site="r_foot_front_ft", name="r_foot_front_gyro"),
    GyroSensorCfg(site="r_foot_rear_ft", name="r_foot_rear_gyro"),
]

cameras_cfg = [
    CameraCfg(name="realsense_depth_camera", site="realsense_depth_frame", fovy=60.0),
    CameraCfg(name="realsense_rgb_camera", site="realsense_rgb_frame", fovy=75.0),
]

cfg = URDFtoMuJoCoLoaderCfg(
    observed_joints=observed_joints,
    actuated_joints=actuated_joints,
    control_modes=control_modes,
    stiffness=stiffness,
    damping=damping,
    gyro_sensors_cfg=gyro_sensors_cfg,
    cameras_cfg=cameras_cfg,
    all_missing_joints_as_sites=True,
)

urdf_string = resolve_robot_model(args.robot_model)
mesh_path = get_mesh_path(ET.parse(urdf_string).getroot())

loader = URDFtoMuJoCoLoader.load_urdf(urdf_string, mesh_path, cfg)

# save xml_str to a file
path = Path(args.output).expanduser()

with open(path, "w") as f:
    f.write(loader.get_mjcf_string())

# include the model in a simple world
world_str = f"""
    <mujoco model="ergoCubWorld">
    <!-- Include your external MJCF file -->
        <include file="{path.resolve()}"/>
    <visual>
        <headlight diffuse="0.6 0.6 0.6" ambient="0.3 0.3 0.3" specular="0 0 0"/>
        <rgba haze="0.15 0.25 0.35 1"/>
        <global azimuth="120" elevation="-20"/>
    </visual>

    <asset>
        <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="3072"/>
        <texture type="2d" name="groundplane" builtin="checker" mark="edge" rgb1="0.2 0.3 0.4" rgb2="0.1 0.2 0.3"
        markrgb="0.8 0.8 0.8" width="300" height="300"/>
        <material name="groundplane" texture="groundplane" texuniform="true" texrepeat="5 5" reflectance="0.2"/>
    </asset>

    <worldbody>
        <light pos="0 0 1.5" dir="0 0 -1" directional="true"/>
        <camera name="default" pos="0.846 -1.465 0.916" xyaxes="0.866 0.500 0.000 -0.171 0.296 0.940"/>
        <geom name="floor" pos="0 0 -0.88" size="0 0 0.05" type="plane" material="groundplane"/>
    </worldbody>
    </mujoco>
    """

# smoke test: load model in Mujoco
model = mujoco.MjModel.from_xml_string(world_str)
data = mujoco.MjData(model)

# visualize the model
if args.contact_forces:
    model.vis.map.force = 0.02
    model.vis.scale.forcewidth = 0.03

    with mujoco.viewer.launch_passive(model, data) as viewer:
        with viewer.lock():
            viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = 1
            viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTFORCE] = 1
            viewer.opt.flags[mujoco.mjtVisFlag.mjVIS_CONTACTSPLIT] = 1
            viewer.opt.frame = mujoco.mjtFrame.mjFRAME_CONTACT
            viewer.opt.label = mujoco.mjtLabel.mjLABEL_CONTACTFORCE

        while viewer.is_running():
            step_start = time.time()

            mujoco.mj_step(model, data)
            viewer.sync()

            dt = model.opt.timestep - (time.time() - step_start)
            if dt > 0:
                time.sleep(dt)
else:
    mujoco.viewer.launch(model=model, data=data)
