clear;
close all;

create_face_vid('Working_with_audio_in_time-Jerry/syl_audio/US114_F60_TG_VSDRC000_Rap_bpm=100_subpb=4_sylLen=0.5_Accapela.wav',...
    'facetest2.mp4');

function create_face_vid(vocalFile,out_vid)
h = figure;
axis tight manual;
% out_vid = 'facetest2.mp4';
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
videoFWriter = vision.VideoFileWriter(out_vid,'FrameRate',out_FPS,'FileFormat','MPEG4');
for i = 1:length(fmvmt)
    curface = bank(:,:,:,fmvmt(i));
    
    imshow(curface,map);
    
    % Capture the plot as an image 
    frame = getframe(h,[100 75 450 450]);
    im = frame2im(frame);
    videoFWriter(im);
end

release(videoFWriter);
end
