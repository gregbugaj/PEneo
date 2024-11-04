
# Inference

```shell
PYTHONPATH=$(pwd) python deploy/inference.py  --model_name_or_path ~/dev/marieai/PEneo/private_pretrained/layoutlmv3-base --dir_image ~/dev/workflow/grapnel-g5/assets/TID-108756/217462777/PID_913_7692_0_217462777/S1  --apply_ocr  --visualize_path  /home/gbugaj/tmp/peneo

```


```shell

PYTHONPATH=$(pwd) python deploy/inference.py  --model_name_or_path ~/dev/marieai/PEneo/private_output/weights/layoutlmv3-base_rfund_en/checkpoint-9000 --dir_image /home/gbugaj/dev/workflow/grapnel-g5/assets/table-frag/001/frag-001.png   --dir_ocr /home/gbugaj/dev/workflow/grapnel-g5/assets/table-frag/001/result.json --visualize_path  /home/gbugaj/tmp/peneo


```

