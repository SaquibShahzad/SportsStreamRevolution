call "setupvars.bat"
if not defined INTEL_OPENVINO_DIR (
    call vcvarsall.bat
)
python openvino_server.py