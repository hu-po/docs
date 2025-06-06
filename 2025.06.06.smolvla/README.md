![thumbnail](thumbnail.png)

# SmolVLA

### Links

**YouTube:** https://youtube.com/live/VbhL8_vVtVM

**X:** https://x.com/i/broadcasts/1lPJqMklwjLJb

**Slides:** https://docs.google.com/presentation/d/1hGropvqiiMCz6bWMunFVnWksmhQMRBY3B4B2kg01hGc/edit?usp=sharing

### References

https://arxiv.org/pdf/2506.01844

https://huggingface.co/blog/smolvla

https://huggingface.co/lerobot/smolvla_base

https://huggingface.co/spaces/Beegbrain/FilterLeRobotData

https://huggingface.co/spaces/lerobot/visualize_dataset?path=%2Flerobot%2Fsvla_so100_sorting%2Fepisode_1

https://arxiv.org/pdf/2303.04137

https://www.physicalintelligence.company/download/pi0.pdf

https://github.com/TheRobotStudio/SO-ARM100

https://arxiv.org/pdf/2503.14734


train (finetune) on 3090
```bash
git clone --depth 1 https://github.com/huggingface/lerobot.git
cd lerobot
uv venv # https://docs.astral.sh/uv/getting-started/installation/
source .venv/bin/activate
uv pip install -e ".[smolvla]"
wandb login
uv run python lerobot/scripts/train.py \
  --policy.path=lerobot/smolvla_base \
  --dataset.repo_id=lerobot/svla_so100_stacking \
  --batch_size=64 \
  --wandb.enable=true \
  --steps=200000
```

eval on 3090
```bash
uv run python smolvla_benchmark.py
Avg inference time: 0.186218 s
Max GPU memory used: 908.43 MB
```


`smolvla_benchmark.py`
```python
import torch
import time
from lerobot.common.policies.smolvla.modeling_smolvla import SmolVLAPolicy
from lerobot.common.policies.smolvla.configuration_smolvla import SmolVLAConfig
from transformers import AutoProcessor

# Load model (replace with your checkpoint if needed)
policy = SmolVLAPolicy.from_pretrained(
    "/home/oop/lerobot/outputs/train/2025-06-05/08-54-14_smolvla/checkpoints/last/pretrained_model"
).to("cuda")
policy.eval()

# Monkey-patch: The loaded policy is missing the language_tokenizer attribute.
policy.language_tokenizer = AutoProcessor.from_pretrained(policy.config.vlm_model_name).tokenizer

# Dummy batch config for a single observation
batch_size = 1
img_shape = (3, 512, 512)  # (C, H, W)
# Infer state_dim from the loaded normalization stats
state_dim = policy.normalize_inputs.buffer_observation_state.mean.shape[-1]

dummy_batch = {
    # a single image observation
    "observation.images.top": torch.rand(batch_size, *img_shape, device="cuda"),
    # a single state observation
    "observation.state": torch.rand(batch_size, state_dim, device="cuda"),
    "task": ["stack the blocks"] * batch_size,
}

# --- Prepare inputs for the model ---
# The policy expects normalized inputs and specific data preparation.
normalized_batch = policy.normalize_inputs(dummy_batch)
images, img_masks = policy.prepare_images(normalized_batch)
state = policy.prepare_state(normalized_batch)
lang_tokens, lang_masks = policy.prepare_language(normalized_batch)
# ---

# Warmup
for _ in range(3):
    with torch.no_grad():
        _ = policy.model.sample_actions(images, img_masks, lang_tokens, lang_masks, state)

# Benchmark
torch.cuda.reset_peak_memory_stats()
start = time.time()
for _ in range(100):
    with torch.no_grad():
        _ = policy.model.sample_actions(images, img_masks, lang_tokens, lang_masks, state)
end = time.time()

print(f"Avg inference time: {(end - start)/100:.6f} s")
print(f"Max GPU memory used: {torch.cuda.max_memory_allocated() / 1024**2:.2f} MB")
```

eval on agx
after cloning lerobot:
- add `OBS_ROBOT = "observation.state"` to `lerobot/lerobot/common/constants.py`
- delete torch from the `pyproject.toml`
```bash
sudo docker run --runtime nvidia -it --rm \
  --network=host \
  -v $PWD:/workspace/lerobot \
  -v $HOME/.cache/huggingface:/root/.cache/huggingface \
  -w /workspace/lerobot \
  dustynv/pytorch:2.1-r36.2.0 \
  bash
pip install --ignore-installed "numpy<2" blinker pyserial
pip install --no-deps -e ".[smolvla]"
pip install --force-reinstall "numpy<2"
pip install --upgrade --force-reinstall transformers
python3 smolvla_benchmark.py
```
https://github.com/dusty-nv/jetson-containers/tree/master/packages/pytorch
