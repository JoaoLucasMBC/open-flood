python ../config/configure_env.py
source ../config/.env
python ../config/create_mount.py
tao model unet train -e $TAO_SPECS_DIR/resnet18/combined_config.txt -r $TAO_EXPERIMENT_DIR/resnet18 -n resnet18 -m $TAO_EXPERIMENT_DIR/pretrained_resnet18/pretrained_semantic_segmentation_vresnet18/resnet_18.hdf5 -k $NVIDIA_API_TOKEN