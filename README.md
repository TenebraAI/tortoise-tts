# AI Voice Cloning for Retards and Savants

This [rentry](https://rentry.org/AI-Voice-Cloning/) aims to serve as both a foolproof guide for setting up AI voice cloning tools for legitimate, local use on Windows, as well as a stepping stone for anons that genuinely want to play around with [TorToiSe](https://github.com/neonbjb/tortoise-tts).

Similar to my own findings for Stable Diffusion image generation, this rentry may appear a little disheveled as I note my new findings with TorToiSe. Please keep this in mind if the guide seems to shift a bit or sound confusing.

>\>Ugh... why bother when I can just abuse 11.AI?

I very much encourage (You) to use 11.AI while it's still viable to use. For the layman, it's easier to go through the hoops of coughing up the $5 or abusing the free trial over actually setting up a TorToiSe environment and dealing with its quirks.

However, I also encourage your own experimentation with TorToiSe, as it's very, very promising, it just takes a little love and elbow grease.

## Glossary

To try and keep the terminology used here (somewhat) consistent and coherent, below are a list of terms, and their definitions (or at least, the way I'm using them):
* `voice cloning`: synthesizing speech to accurately replicate a subject's voice.
* `input clips` / `voice clips` / `audio input` / `voice samples` : the original voice source of the subject you're trying to clone.
* `waveform`: the raw audio.
* `sampling rate`: the bandwidth of a given waveform, represented as twice the frequency of the waveform it represents.
* `voice latents` / `conditional latents` / `latents`: computated traits of a voice.
* `autoregressive samples` (`samples` / `tokens`): the initial generation pass to output tokens, and (usually) the most computationally expensive. More samples = better "cloning".
* `CLVP`: Contrastive Language-Voice Pretraining: an analog to CLIP, but for voices. After the autoregressive samples pass, those samples/tokens are compared against the CLVP to find the best candidates.
* `CVVP`: Contrastive Voice-Voice Pretraining: a (deprecated) model that can be used weighted in junction with the CLVP.
* `candidates`: results from the comparing against the CLVP/CVVP models. (Assumed to be) ordered from best to worst.
* `diffusion decoder` / `vocoder`: these passes are responsible for encoding the tokens into a MEL spectrogram into a waveform.
* `diffusion iterations`: how many passes to put into generating the output waveform. More iterations = better audio quality.
* `diffusion sampler` / `sampler`: the sampling method used during the diffusion decoding pass, albeit a bit of a misnomer. Currently, only two samplers are implemented.

## Modifications

My fork boasts the following additions, fixes, and optimizations:
* a competent web UI made in Gradio to expose a lot of tunables and options
* cleaned up output structure of resulting audio files
* caching computed conditional latents for faster re-runs
	- additionally, regenerating them if the script detects they're out of date
* uses the entire audio sample instead of the first four seconds of each sound file for better reproducing
* activated unused DDIM sampler
* use of some optimizations like `kv_cache`ing for the autoregression sample pass, and keeping data on GPU 
* compatibilty with DirectML
* easy install scripts
* and more!

## Colab Notebook

A colab notebook to quickly set up and use this repo is included and available [here](https://colab.research.google.com/drive/1v2yTl-VkhYRflBUND-I9NuVWmCa5HeOg?usp=share_link): https://colab.research.google.com/drive/1v2yTl-VkhYRflBUND-I9NuVWmCa5HeOg

For the unfortunate using Paperspace, this notebook should also work for it.

## Installing

Outside of the very small prerequisites, everything needed to get TorToiSe working is included in the repo.

### Pre-Requirements

Windows:
* ***Python 3.9***: https://www.python.org/downloads/release/python-3913/
	- I cannot stress this hard enough. PyTorch under Windows requires a very specific version.
	- you *might* be able to get away with this if you're not using CUDA as a backend, but I cannot make any promises.
* Git (optional): https://git-scm.com/download/win
* CUDA drivers, if NVIDIA

Linux:
* python3.x (tested with 3.10)
* git
* ROCm for AMD, CUDA for NVIDIA

### Setup

#### Windows

Download Python and Git and run their installers.

After installing Python, open the Start Menu and search for `Command Prompt`. Type `cd `, then drag and drop the folder you want to work in (experienced users can just `cd <path>` directly), then hit Enter.

Paste `git clone https://git.ecker.tech/mrq/tortoise-tts` to download TorToiSe and additional scripts, then hit Enter. Inexperienced users can just download the repo as a ZIP, and extract.

Afterwards, run the setup script, depending on your GPU, to automatically set things up.
* AMD: `setup-directml.bat`
* NVIDIA: `setup-cuda.bat`

If you've done everything right, you shouldn't have any errors.

##### Note on DirectML Support

PyTorch-DirectML is very, very experimental and is still not production quality. There's some headaches with the need for hairy kludgy patches.

These patches rely on transfering the tensor between the GPU and CPU as a hotfix for some unimplemented functions, so performance is definitely harmed.

Both half precision (float16) and use of `kv_cache`ing for the autoregressive sampling pass are disabled when using DirectML
* I haven't been assed to find an (elegant) autocast to float16 for the DirectML backend
* `kv_cache`ing will silently crash the program if used

Both the conditional latent computation and the vocoder pass have to be done on the CPU entirely because of some quirks with DirectML:
* computing conditional latents will outright crash, I forget the error
* performing the vocoder on the GPU will produce garbage audio

On my 6800XT, VRAM usage climbs almost the entire 16GiB, so be wary if you OOM somehow. The `Low VRAM` flag may NOT have any additional impact from the constant copying anyways, as the models and tensors already swap between CPU and GPU.

For AMD users, I still might suggest using Linux+ROCm as it's (relatively) headache free, but I had stability problems.

#### Linux

First, make sure you have both `python3.x` and `git` installed, as well as the required compute platform according to your GPU (ROCm or CUDA).

Simply run the following block:

```
git clone https://git.ecker.tech/mrq/tortoise-tts
cd tortoise-tts
chmod +x *.sh
```

Then, depending on your GPU:
* AMD: `./setup-rocm.sh`
* NVIDIA: `./setup-cuda.sh`

And you should be done!

### Updating

To check for updates, simply run `update.bat` (or `update.sh`). It should pull from the repo, as well as fetch for any new dependencies.

If, for some reason, you manage to be quick on the trigger to update when I reverse a commit and you get an error trying to run the update script, run `update-force.bat` (or `update-force.sh`) to force an update.

### Pitfalls You May Encounter

I'll try and make a list of "common" (or what I feel may be common that I experience) issues with getting TorToiSe set up:
* `CUDA is NOT available for use.`: If you're on Linux, you failed to set up CUDA (if NVIDIA) or ROCm (if AMD). Please make sure you have these installed on your system.
	- If you're on Windows with an AMD card, you're stuck out of luck, as ROCm is not available on Windows (without major hoops to be jumped). If you're on an NVIDIA GPU, then I'm not sure what went wrong.
* `failed reading zip archive: failed finding central directory`: You had a file fail to download completely during the model downloading initialization phase. Please open either `.\models\tortoise\` or `.\models\transformers\`, and delete the offending file.
	- You can deduce what that file is by reading the stack trace. A few lines above the last like will be a line trying to read a model path.
* `torch.cuda.OutOfMemoryError: CUDA out of memory.`: You most likely have a GPU with low VRAM (~4GiB), and the small optimizations with keeping data on the GPU is enough to OOM. Please open the `start.bat` file and add `--low-vram` to the command (for example: `py app.py --low-vram`) to disable those small optimizations.
* `WavFileWarning: Chunk (non-data) not understood, skipping it.`: something about your WAVs are funny, and its best to remux your audio files with FFMPEG (included batch file in `.\convert\`).
	- Honestly, I don't know if this does impact output quality, as I feel it's placebo when I do try and correct this.
* `Unable to find a valid cuDNN algorithm to run convolution`: a rather weird error message that occurs in the colab notebook. The vanilla auto-batch size calculation is a bit flawed, so try and reduce it to a fixed number in `Settings`, like eight or so.

#### Non-"""Issues"""

I hate to be a hardass over it, but below are some errors that come from not following my instructions:
* `Could not find a version that satisfies the requirement torch (from versions: none)`: you are using an incorrect version of python. Please install the linked python3.9.
* `Failed to import soundfile. 'soundfile' backend is not available.`: you are most likely using conda (or miniconda), an environment I do not support anymore due to bloat. Please install the linked python3.9, or try [this](https://github.com/librosa/librosa/issues/1117#issuecomment-907853797).
	- I used to have a setup script using conda as an environment, but it's bloat and a headache to use, so I can't keep it around.
* `No hardware acceleration is available, falling back to CPU...`: you do not have a CUDA runtime/drivers installed. Please install them.
	- I do not have a link for it, as it literally worked on my machine with the basic drivers for my 2060.

If you already have a `tortoise-venv` folder after installing the correct python version, delete that folder, as it will still use the previous version of python.

## Preparing Voice Samples

Now that the tough part is dealt with, it's time to prepare voice clips to use.

Unlike training embeddings for AI image generations, preparing a "dataset" for voice cloning is very simple.

As a general rule of thumb, try to source clips that aren't noisy, solely the subject you are trying to clone, and doesn't contain any non-words (like yells, guttural noises, etc.). If you must, run your source through a background music/noise remover (how to is an exercise left to the reader). It isn't entirely a detriment if you're unable to provide clean audio, however. Just be wary that you might have some headaches with getting acceptable output.

Nine times out of ten, you should be fine using as many clips as possible. There's no hard specifics on how many, or how long, your sources should be.

However, keep in mind how you combine/separate your clips; depending on the mode to calculate a voice's conditional latents:
* you might suffer from reduced throughput, as the smallest voice file will be used as the size of best fit
* a voice might get split mid-word, affecting how the latents are computed, as each batch is averaged together

For safety, try to keep your clips within the same length, or increase your `Voice Latents Max Chunk Size`, if console output alerts the best fit size exceeds this.

If you're looking to trim your clips, in my opinion, ~~Audacity~~ Tenacity works good enough, as you can easily output your clips into the proper format (22050 Hz sampling rate).

Power users with FFMPEG already installed can simply used the provided conversion script in `.\convert\`.

After preparing your clips as WAV files at a sample rate of 22050 Hz, open up the `tortoise-tts` folder you're working in, navigate to the `voices` folder, create a new folder in whatever name you want, then dump your clips into that folder. While you're in the `voice` folder, you can take a look at the other provided voices.

**!**NOTE**!**: Before 2023.02.10, voices used to be stored under `.\tortoise\voices\`, but has been moved up one folder. Compatibily is maintained with the old voice folder, but will take priority.

## Using the Software

Now you're ready to generate clips. With the command prompt still open, simply enter `start.bat` (or `start.sh`), and wait for it to print out a URL to open in your browser, something like `http://127.0.0.1:7860`.

If you're looking to access your copy of TorToiSe from outside your local network, tick the `Public Share Gradio` button in the `Settings` tab, then restart.

### Generate

You'll be presented with a bunch of options in the default `Generate` tab, but do not be overwhelmed, as most of the defaults are sane, but below are a rough explanation on which input does what:
* `Prompt`: text you want to be read. You wrap text in `[brackets]` for "prompt engineering", where it'll affect the output, but those words won't actually be read.
* `Line Delimiter`: String to split the prompt into pieces. The stitched clip will be stored as `combined.wav`
	- Setting this to `\n` will generate each line as one clip before stitching it. Leave blank to disable this.
* `Emotion`: the "emotion" used for the delivery. This is a shortcut to utilizing "prompt engineering" by starting with `[I am really <emotion>,]` in your prompt. This is merely a suggestion, not a guarantee.
* `Custom Emotion + Prompt`: a non-preset "emotion" used for the delivery. This is a shortcut to utilizing "prompt engineering" by starting with `[<emotion>]` in your prompt.
* `Voice`: the voice you want to clone. You can select `microphone` if you want to use input from your microphone.
* `Microphone Source`: Use your own voice from a line-in source.
* `Reload Voice List`: refreshes the voice list and updates. ***Click this*** after adding or removing a new voice.
* `(Re)Compute Voice Latents`: regenerates a voice's cached latents.
* `Experimental Compute Latents Mode`: this mode will combine all voice samples into one file, then split it evenly (if under the maximum allowed chunk size under `Settings`)

Below are a list of generation settings:
* `Candidates`: number of outputs to generate, starting from the best candidate. Depending on your iteration steps, generating the final sound files could be cheap, but they only offer alternatives to the samples generated to pull from (in other words, the later candidates perform worse), so don't be compelled to generate a ton of candidates.
* `Seed`: initializes the PRNG to this value. Use this if you want to reproduce a generated voice.
* `Preset`: shortcut values for sample count and iteration steps. Clicking a preset will update its corresponding values. Higher presets result in better quality at the cost of computation time.
* `Samples`: analogous to samples in image generation. More samples = better resemblance / clone quality, at the cost of performance. This strictly affects clone quality.
* `Iterations`: influences audio sound quality in the final output. More iterations = higher quality sound. This step is relatively cheap, so do not be discouraged from increasing this. This strictly affects quality in the actual sound.
* `Temperature`: how much randomness to introduce to the generated samples. Lower values = better resemblance to the source samples, but some temperature is still required for great output.
	- I assume this affects variance between candidates. Very low temperatures will have very low variety between candidates. Very high temperatures will have large nuances between candidates.
	- **!**NOTE**!**: This value is very inconsistent and entirely depends on the input voice. In other words, some voices will be receptive to playing with this value, while others won't make much of a difference.
	- **!**NOTE**!**: some voices will be very receptive to this, where it speaks slowly at low temperatures, but nudging it a hair and it speaks too fast.
* `Pause Size`: Governs how large pauses are at the end of a clip (in token size, not seconds). Increase this if your output gets cut off at the end.
	- **!**NOTE**!**: too large of a pause size can lead to unexpected behavior.
* `Diffusion Sampler`: sampler method during the diffusion pass. Currently, only `P` and `DDIM` are added, but does not seem to offer any substantial differences in my short tests.
	`P` refers to the default, vanilla sampling method in `diffusion.py`.
	To reiterate, this ***only*** is useful for the diffusion decoding path, after the autoregressive outputs are generated.

Below are an explanation of experimental flags. Messing with these might impact performance, as these are exposed only if you know what you are doing.
* `Half-Precision`: (attempts to) hint to PyTorch to auto-cast to float16 (half precision) for compute. Disabled by default, due to it making computations slower.
* `Conditional Free`: a quality boosting improvement at the cost of some performance. Enabled by default, as I think the penaly is negligible in the end.
* `CVVP Weight`: governs how much weight the CVVP model should influence candidates. The original documentation mentions this is deprecated as it does not really influence things, but you're still free to play around with it.
	Currently, setting requires regenerating your voice latents, as I forgot to have it return some extra data that weighing against the CVVP model uses. Oops.
	Setting this to 1 leads to bad behavior.
* `Top P`: P value used in nucleus sampling; lower values mean the decoder produces more "likely" (aka boring) outputs.
* `Diffusion Temperature`: the variance of the noise fed into the diffusion model; values at 0 are the "mean" prediction of the diffusion network and will sound bland and smeared.
* `Length Penalty`: a length penalty applied to the autoregressive decoder; higher settings causes the model to produce more terse outputs.
* `Repetition Penalty`: a penalty that prevents the autoregressive decoder from repeating itself during decoding. Can be used to reduce the incidence of long silences or "uhhhhhhs", etc.
* `Conditioning-Free K`: determintes balancing the conditioning free signal with the conditioning-present signal. 

After you fill everything out, click `Run`, and wait for your output in the output window. The sampled voice is also returned, but if you're using multiple files, it'll return the first file, rather than a combined file.

All outputs are saved under `./result/[voice name]/[timestamp]/` as `result.wav`, and the settings in `input.txt`. Depending on the browser you're using, you'll be able to see an audio player in the output section of the UI. Clicking on the vertical ellipsis button should bring up the option to download the audio and control the playback speed.

To save you from headaches, I strongly recommend playing around with shorter sentences first to find the right values for the voice you're using before generating longer sentences.

As a quick optimization, I modified the script to have the `conditional_latents` are saved after loading voice samples, and subsequent uses will load that file directly (at the cost of not returning the `Sample voice` to the web UI). Additionally, these `conditional_latents` are also computed in a way to use the entire clip, rather than the first four seconds the original tortoise-tts uses. If there's voice samples that have a modification time newer than this cached file, it'll skip loading it and load the normal WAVs instead.

**!**NOTE**!**: cached `latents.pth` files generated before 2023.02.05 will be ignored, due to a change in computing the conditiona latents. This *should* help bump up voice cloning quality. Apologies for the inconvenience.

### History

In this tab, a rudimentary way of viewing past results can be found here.

With it, you just select a voice, then you can quickly view their generation settings.

To play a file, select a specific file with the second dropdown list.

To reuse a voice file's settings, click `Copy Settings`.

### Utilities

In this tab, you can find some helper utilities that might be of assistance.

For now, an analog to the PNG info found in Voldy's Stable Diffusion Web UI resides here. With it, you can upload an audio file generated with this web UI to view the settings used to generate that output. Additionally, the voice latents used to generate the uploaded audio clip can be extracted.

If you want to reuse its generation settings, simply click `Copy Settings`.

To import a voice, click `Import Voice`. Remember to click `Refresh Voice List` in the `Generate` panel afterwards, if it's a new voice.

### Settings

This tab (should) hold a bunch of other settings, from tunables that shouldn't be tampered with, to settings pertaining to the web UI itself.

Below are settings that override the default launch arguments. Some of these require restarting to work.
* `Listen`: sets the hostname, port, and/or path for the web UI to listen on.
	- For example, `0.0.0.0:80` will have the web UI accept all connections on port 80
	- For example, `10.0.0.1:8008/gradio` will have the web UI only accept connections through `10.0.0.1`, at the path `/gradio`
* `Public Share Gradio`: Tells Gradio to generate a public URL for the web UI. Ignored if specifying a path through the `Listen` setting.
* `Check for Updates`: checks for updates on page load and notifies in console. Only works if you pulled this repo from a gitea instance.
* `Only Load Models Locally`: enforces offline mode for loading models. This is the equivalent of setting the env var: `TRANSFORMERS_OFFLINE`
* `Low VRAM`: disables optimizations in TorToiSe that increases VRAM consumption. Suggested if your GPU has under 6GiB.
* `Embed Output Metadata`: enables embedding the settings and latents used to generate that audio clip inside that audio clip. Metadata is stored as a JSON string in the `lyrics` tag.
* `Slimmer Computed Latents`: falls back to the original, 12.9KiB way of storing latents (without the extra bits required for using the CVVP model).
* `Voice Fixer`: runs each generated audio clip through `voicefixer`, if available and installed.
* `Voice Latent Max Chunk Size`: during the voice latents calculation pass, this limits how large, in bytes, a chunk can be. Large values can run into VRAM OOM errors.
* `Sample Batch Size`: sets the batch size when generating autoregressive samples. Bigger batches result in faster compute, at the cost of increased VRAM consumption. Leave to 0 to calculate a "best" fit.
* `Concurrency Count`: how many Gradio events the queue can process at once. Leave this over 1 if you want to modify settings in the UI that updates other settings while generating audio clips.
* `Output Sample Rate`: the sample rate to save the generated audio as. It provides a bit of slight bump in quality
* `Output Volume`: adjusts the volume through amplitude scaling

## Example(s)

Below are some (rather outdated) outputs I deem substantial enough to share. As I continue delving into TorToiSe, I'll supply more examples and the values I use.

Source (Patrick Bateman): 
* https://files.catbox.moe/skzumo.zip

Output (`My name is Patrick Bateman.`, `fast` preset):
* https://files.catbox.moe/cw88t5.wav
* https://files.catbox.moe/bwunfo.wav
* https://files.catbox.moe/ppxprv.wav

I trimmed up some of the samples to end up with ten short clips of about 10 seconds each. With a 2060, it took a hair over a minute to generate the initial samples, then five to ten seconds for each clip of a total of three. Not too bad for something running on consumer grade shitware.

Source (Harry Mason):
* https://files.catbox.moe/n2xor1.mp3
* https://files.catbox.moe/bbfke3.mp3

Output (The McDonalds building creepypasta, custom preset of 128 samples, 256 iterations):
* https://voca.ro/16XSgdlcC5uT

This took quite a while, over the course of a day half-paying-attention at the command prompt to generate the next piece. I only had to regenerate one section that sounded funny, but compared to 11.AI requiring tons of regenerations for something usable, this is nice to just let run and forget. Initially he sounds rather passable as Harry Mason, but as it goes on it seems to kinda falter. Sound effects and music are added in post and aren't generated by TorToiSe.

Source (James Sunderland):
* https://files.catbox.moe/ynoeld.mp3
* https://files.catbox.moe/lxgbsm.mp3

Output (The McDonalds building creepypasta, 256 samples, 256 iterations, 0.1 temp, pause size 8, DDIM, conditioning free, seed 1675690127):
* https://vocaroo.com/1nXmip0oJu8Z

This took a while to generate while I slept (and even managed to wake up before it finished). Using the batch function, this took 6.919 hours on my 2060 to generate the 27 pieces with zero editing on my end.

I'm providing this even with its nasty warts to highlight the quirks: the weird gaps where there's a strange sound instead, the random pauses for "thought", etc.

I think this also highlights how just combining your entire source sample gung-ho isn't a good idea, as he's not as high of a pitch in his delivery compared to how he usually is throughout most of the game (a sort of average between his two ranges). I can't gauge how well it did in reproducing it, since my ears are pretty much burnt out from listening to so many clips, but I believe he's pretty believable as a James Sunderland.

Output (`Is that really you, Mary?`, Ultra Fast preset, settings and latents embedded)
* https://files.catbox.moe/gy1jvz.wav

This was just a quick test for an adjustable setting, but this one turned out really nice (for being a quick test) on the off chance. It's not the original delivery, and it definitely sounds robotic still, but it's on the Ultra Fast preset, as expected.

## Caveats (and Upsides)

To me, I find a few problems with TorToiSe over 11.AI:
* computation time is quite an issue. Despite Stable Diffusion proving to be adequate on my 2060, TorToiSe takes quite some time with modest settings.
	- However, on my 6800XT, performance was drastically uplifted due to having more VRAM for larger batch sizes (at the cost of Krashing).
* reproducability in a voice depends on the "compatibilty" with the model TorToiSe was trained on.
	- However, this also appears to be similar to 11.AI, where it was mostly trained on audiobook readings.
* the lack of an obvious analog to the "stability" and "similarity" sliders kind of sucks, but it's not the end of the world.
	However, the `temperature` option seems to prove to be a proper analog to either of these.

Although, I can look past these as TorToiSe offers, in comparison to 11.AI:
* the "speaking too fast" issue does not exist with TorToiSe. I don't need to fight with it by pretending I'm a Gaia user in the early 2000s by sprinkling ellipses.
* the overall delivery seems very natural, sometimes small, dramatic pauses gets added at the legitimately most convenient moments, and the inhales tend to be more natural. Many of vocaroos from 11.AI where it just does not seem properly delivered.
* being able to run it locally means I do not have to worry about some Polack seeing me use the "dick" word.