function [vidFile, mixFile] = face_move_envelope(rapFile, beatFile, gifFile)
    [rapPath,~] = fileparts(rapFile);
    [beatPath,~] = fileparts(beatFile);
    [gifPath,~] = fileparts(gifFile);
    addpath(rapPath, beatPath, gifPath);

    % create_face_vid('/home/deepcut/flowtron/results/rapsid0_sigma0.5.wavsid0_sigma0.5.wav_Rap_bpm=100_subpb=4_sylLen=1_Accapela.wav',...
    %     '/home/deepcut/flowtron/results/rap.avi');
    vidFile = create_face_vid(rapFile, gifFile);
    mixFile = mix_beat(rapFile, beatFile);
end

function [mixFile] = mix_beat(rapFile, beatFile)
    [rap, ~] = audioread(rapFile);
    [beat, FSb] = audioread(beatFile);
    [rapPath,rapName,rapExt] = fileparts(rapFile);
    [~,beatName,~] = fileparts(beatFile);
    mixFile = fullfile(rapPath, [rapName beatName rapExt]);
    rap = resample(rap,441,160);
    mix = rap + beat(1:length(rap)) / 2;
    audiowrite(mixFile,mix,FSb)
end


function [vidFile] = create_face_vid(rapFile, gifFile)
    out_FPS = 60;

    [vocal,Fs] = audioread(rapFile);

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
    
    % Define output filename
    [rapPath,rapName,~] = fileparts(rapFile);
    [~,gifName,~] = fileparts(gifFile);
    vidFile = fullfile(rapPath, [rapName '+' gifName '.avi']);
    
    % Write video as .avi for later reencoding
    ims = zeros(720,720,3,length(fmvmt));
    try
        parpool(4);
    catch
        warning('Not sure if parfor will break');
    end
    parfor i = 1:length(fmvmt)
        h =figure('Renderer', 'painters', 'Position', [10 10  900 899], 'visible', 'off') ;
        a = axes('Position',[0.1 0.1 0.8 0.8]); % for 720 x 720 output from 900 x 900 figure
        axis tight manual;
    
        curface = bank(:,:,:,fmvmt(i));

        imshow(curface,map);

        % Capture the plot as an image
        frame = getframe(a);
        ims(:,:,:,i) = frame2im(frame);
        close(h)
    end
    
    videoFWriter = vision.VideoFileWriter(vidFile,'FrameRate',out_FPS,'FileFormat','AVI');
    for i = 1:length(fmvmt)
        im = ims(:,:,:,i);
        videoFWriter(uint8(im));
    end
    release(videoFWriter);
end
