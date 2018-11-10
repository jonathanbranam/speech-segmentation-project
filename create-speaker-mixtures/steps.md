# Steps to get this working

1. Install GNU octave
  * I used `brew install octave` on OS X
2. Install required octave packages

```
pkg install -forge control
pkg install -forge signal
```

3. Change paths in files

```matlab
wsj0root = '/Volumes/user/jbranam/files/study/iums/E511_MLSP/project/data/wsj0-merged/';
output_dir16k='/Volumes/user/jbranam/files/study/iums/E511_MLSP/project/data/wsj0-mix/2speakers/wav16k';
output_dir8k='/Volumes/user/jbranam/files/study/iums/E511_MLSP/project/data/wsj0-mix/2speakers/wav8k';
```

4. Make sure octave packages are loaded

I added the following lines to the `create_wav_2speakers.m` file

```matlab
if (exist ("OCTAVE_VERSION", "builtin") > 0)
  pkg load control
  pkg load signal
end
```
4. Profit
