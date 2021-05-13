function [vidFile, mixFile] = face_move_envelope(rapFile, beatFile, gifFile, bpm)
    bpm = str2num(bpm);
    [rapPath,~] = fileparts(rapFile);
    [beatPath,~] = fileparts(beatFile);
    [gifPath,~] = fileparts(gifFile);
    addpath(rapPath, beatPath, gifPath);
    
    [rap, FSr] = audioread(rapFile);
    [beat, FSb] = audioread(beatFile);
    [rapPath,rapName,rapExt] = fileparts(rapFile);
    [~,beatName,~] = fileparts(beatFile);
    
    % Pad rap with one measure of silence at beginning and end
    measureLen = 4 * FSr * 60 / bpm;
    pad = zeros(round(measureLen),1);
    rap = [pad; rap; pad];
    
    % Define output filename
    [~,gifName,~] = fileparts(gifFile);
    vidFile = fullfile(rapPath, [rapName '+' gifName '.avi']);
    mixFile = fullfile(rapPath, [rapName beatName rapExt]);
    
    mix_beat(mixFile, rap, beat, FSr, FSb);
    create_face_vid(vidFile, rap, FSr, gifFile);
end

function mix_beat(mixFile, rap, beat, FSr, FSb)
    
    rap = resample(rap,FSb,FSr);
    beat = [beat; beat];
    mix = 0.5.*rap + beat(1:length(rap)) / 2;
    audiowrite(mixFile,mix,FSb)
end


function  create_face_vid(vidFile, vocal, Fs, gifFile)
    out_FPS = 60;

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
    [bank,map] = imread(gifFile,'frames','all');
    bank = bank(:,:,:,1:4);
    
 
    % Write video as .avi for later reencoding
    % ims = zeros(720,720,3,length(fmvmt));
    ims = zeros(36,36,3,length(fmvmt));
    outdim = size(ims);
    try
        parpool(4);
    catch
        warning('Not sure if parfor will break');
    end
    parfor i = 1:length(fmvmt)
        %h =figure('Renderer', 'painters', 'Position', [10 10  900 899], 'visible', 'off') ;
        h =figure('Renderer', 'painters', 'Position', [10 10 44 45 ], 'visible', 'off') ;
        a = axes('Position',[0.1 0.1 0.8 0.8]); % for 720 x 720 output from 900 x 900 figure
                                                % for 36x36 output from 45x45 figure?
        axis tight manual;
    
        curface = bank(:,:,:,fmvmt(i));

        imshow(curface,map);

        % Capture the plot as an image
        frame = getframe(a);
        im = frame2im(frame)
        ims(:,:,:,i) = im(2:end,:,:); % Indexing because padding from fig still present
        close(h)
    end
    
    videoFWriter = vision.VideoFileWriter(vidFile,'FrameRate',out_FPS,'FileFormat','AVI');
    for i = 1:length(fmvmt)
        im = ims(:,:,:,i);
        videoFWriter(uint8(im));
    end
    release(videoFWriter);
end
