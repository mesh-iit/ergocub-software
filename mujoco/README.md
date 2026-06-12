# ergoCub MuJoCo XML Generation

This folder contains `generate_ergoCub_xml.py`, a script that generates a MuJoCo XML description for the selected ergoCub robot model and opens it in the MuJoCo viewer.

The script relies on [mujoco-urdf-loader](https://github.com/gbionics/mujoco-urdf-loader) to convert the robot URDF into MJCF, then post-processes the result to add actuators, sensors, hand constraints, camera frames, and the MuJoCo world wrapper.

## Requirements

`mujoco-urdf-loader` needs to be installed following these instructions:
- https://github.com/gbionics/mujoco-urdf-loader#installation

## How To Run

Once done, first activate the conda env:

```bash
conda activate mujocoloaderenv
```

then:

```bash
python generate_ergoCub_xml.py
```

By default, the script loads `ergoCubSN001`, writes the MJCF model to `ergocub.xml`, and enables contact-force visualization in the viewer.

### Options

```bash
python generate_ergoCub_xml.py [--robot-model ROBOT_MODEL] [--output OUTPUT] [--contact-forces | --no-contact-forces]
```

- `--robot-model`: robot model to load. It can be:
  - a model name under `package://ergoCub/robots`, such as `ergoCubSN001`
  - a serial-number shorthand starting with `SN`, such as `SN001`
  - a full package URI, such as `package://ergoCub/robots/ergoCubSN001/model.urdf`
  - a local URDF path
- `--output`: path where the generated MJCF XML file is written. The default is `ergocub.xml`.
- `--contact-forces` / `--no-contact-forces`: enable or disable contact-force visualization in the MuJoCo viewer. Contact forces are enabled by default.

Examples:

```bash
python generate_ergoCub_xml.py --robot-model SN001
python generate_ergoCub_xml.py --robot-model ergoCubSN001 --output ergocub_sn001.xml
python generate_ergoCub_xml.py --robot-model package://ergoCub/robots/ergoCubSN001/model.urdf
python generate_ergoCub_xml.py --robot-model /path/to/model.urdf --no-contact-forces
```

What the script does:

1. Loads the ergoCub URDF through `mujoco-urdf-loader`.
2. Converts it into MJCF.
3. Writes the generated model to the path selected with `--output`.
4. Wraps the model in a simple MuJoCo world with a floor, lights, and a camera.
5. Opens the result in the MuJoCo viewer, optionally showing contact-force visualizations.

## Output

After a successful run, you should get:

- the generated MJCF XML file at the selected output path, `ergocub.xml` by default
- a MuJoCo viewer window showing the robot

## Notes

- The default robot model is resolved from `package://ergoCub/robots/ergoCubSN001/model.urdf`.
- Relative output paths are resolved from the directory where the script is executed.
- If MuJoCo cannot find the mesh files, check that the `meshdir` attribute in `ergocub.xml` points to the correct local mesh directory.
- If the viewer does not open, make sure your environment has GUI support.
- If Python cannot import `mujoco_urdf_loader`, install it into the active environment or add the repository to `PYTHONPATH`.
