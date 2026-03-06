# AGENTS.md

## Cursor Cloud specific instructions

This is a Python CLI tool ("Meme Generator") that creates GIFs from YouTube videos using yt-dlp, OpenAI Whisper, and FFmpeg. See `README.md` for usage.

### Key environment notes

- **Python venv**: The virtual environment is at `venv/`. Activate with `source venv/bin/activate`.
- **CPU-only PyTorch**: The cloud VM has no GPU, so `torch` must be the CPU variant (`torch==2.8.0+cpu` from `https://download.pytorch.org/whl/cpu`). The default `requirements.txt` installs the CUDA build which will fail to import on CPU-only machines.
- **`ffmpeg` vs `ffmpeg-python` conflict**: Both `ffmpeg==1.4` and `ffmpeg-python==0.2.0` are listed in `requirements.txt` and both provide a Python module named `ffmpeg`. The script uses `ffmpeg-python`'s API (`ffmpeg.input()`, `ffmpeg.run()`, `ffmpeg.output()`). After installing from `requirements.txt`, uninstall the conflicting `ffmpeg==1.4` package: `pip uninstall -y ffmpeg`.
- **YouTube bot detection**: YouTube blocks automated downloads from cloud VMs. The yt-dlp download step will fail without browser cookies. To test the full pipeline without YouTube, create a synthetic video with FFmpeg and run each step manually (audio extraction, Whisper transcription, GIF generation).
- **yt-dlp + deno**: Newer yt-dlp versions require a JavaScript runtime (deno). Install via `pip install deno`.
- **No linter/tests**: This project has no linter config, test framework, or automated tests. Verification is done by running the script or testing individual pipeline components.

### Running the script

```bash
source venv/bin/activate
python generate_meme.py
```

The script prompts for: YouTube URL, subtitle preference (y/n), font size. Output is `output.gif`.
