python ../config/configure_env.py
source ../config/.env
python ../config/create_mount.py
tao model unet inference -e $TAO_SPECS_DIR/resnet18/combined_config.txt -m $TAO_EXPERIMENT_DIR/resnet18/weights/resnet18.tlt -o $TAO_PROJECT_DIR/tao_infer_testing -k $NVIDIA_API_KEY