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

eval on agx
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

after cloning lerobot:
- add `OBS_ROBOT = "observation.state"` to `lerobot/lerobot/common/constants.py`
- delete torch from the `pyproject.toml`
- create `smolvla_benchmark.py`

```python
import torch
import time
from lerobot.common.policies.smolvla.modeling_smolvla import SmolVLAPolicy
from lerobot.common.policies.smolvla.configuration_smolvla import SmolVLAConfig

# Load model (replace with your checkpoint if needed)
policy = SmolVLAPolicy.from_pretrained("lerobot/smolvla_base").to("cuda")

# Dummy batch config (adjust as needed)
batch_size = 1
n_obs_steps = policy.config.n_obs_steps
img_shape = (3, 512, 512)  # (C, H, W)
state_dim = policy.config.max_state_dim

# Create dummy batch
dummy_batch = {
    "observation.images.top": torch.rand(batch_size, n_obs_steps, *img_shape, device="cuda"),
    "observation.state": torch.rand(batch_size, n_obs_steps, state_dim, device="cuda"),
    "task": ["stack the blocks"] * batch_size,
}

# Warmup
for _ in range(3):
    with torch.no_grad():
        _ = policy.select_action(dummy_batch)

# Benchmark
torch.cuda.reset_peak_memory_stats()
start = time.time()
for _ in range(100):
    with torch.no_grad():
        _ = policy.select_action(dummy_batch)
end = time.time()

print(f"Avg inference time: {(end - start)/100:.6f} s")
print(f"Max GPU memory used: {torch.cuda.max_memory_allocated() / 1024**2:.2f} MB")
```