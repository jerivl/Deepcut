clear;
close all;

% create_face_vid('/home/deepcut/flowtron/results/rapsid0_sigma0.5.wavsid0_sigma0.5.wav_Rap_bpm=100_subpb=4_sylLen=1_Accapela.wav',...
%     '/home/deepcut/flowtron/results/rap.avi');
create_face_vid('sid0_sigma0.5.wav_Rap_bpm=100_subpb=4_sylLen=0.5_Accapela.wav','rap.avi');
mix_beat('sid0_sigma0.5.wav_Rap_bpm=100_subpb=4_sylLen=0.5_Accapela.wav','beat1.wav')

command1 = 'ffmpeg -i /home/deepcut/deepcut/src/rap.avi -i /home/deepcut/deepcut/src/mix.wav -c:v copy -c:a aac /home/deepcut/deepcut/src/done.avi -y';
command2 = 'ffmpeg -i /home/deepcut/deepcut/src/done.avi /home/deepcut/deepcut/src/done.mp4 -y';
system(command1);
system(command2);

function mix_beat(rapFile, beatFile)
    [rap, FSr] = audioread(rapFile);
    [beat, FSb] = audioread(beatFile);
    rap = resample(rap,441,160);
    mix = rap + beat(1:length(rap)) / 2;
    audiowrite('mix.wav',mix,FSb)
end


function create_face_vid(vocalFile,out_vid)
    h = figure;
    axis tight manual;
    out_FPS = 60;

    [vocal,Fs] = audioread(vocalFile);

    % Take envelope and smooth
    dRC = compressor(-25,10,'AttackTime',0,'ReleaseTime',0);
    % visualize(dRC)
    env = dRC(vocal);
    env = envelope(env);
    env = movmedian(env,1000);
    env = movmean(env,500);
    env = movmean(env,1000);

    % Quantize to 4 face positions
    fmvmt = 4.*env./max(env);
    fmvmt = resample(fmvmt,out_FPS,Fs);
    fmvmt = round(fmvmt) + 1;
    fmvmt(fmvmt > 4) = 4;

    % Get 4 face positions
    [bank,map] = imread('Face 005.gif','frames','all');
    bank = bank(:,:,:,1:4);
    videoFWriter = vision.VideoFileWriter(out_vid,'FrameRate',out_FPS,'FileFormat','AVI');
    for i = 1:length(fmvmt)
        curface = bank(:,:,:,fmvmt(i));

        imshow(curface,map);

        % Capture the plot as an image
        frame = getframe(h,[100 75 700 700]);
        im = frame2im(frame);
        videoFWriter(im);
    end

    release(videoFWriter);
end
