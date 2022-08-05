%% Clean fMRI data for fc analaysis 
clear all;

subjects = [14, 16, 18, 22, 27, 41, 45, 46, 55, 60];

for i = 1:length(subjects)
    sub = subjects(i);
    
    base = ['/projects/b1081/member_directories/zladwig/neurohackademy/Nifti/derivatives/preproc_fmriprep-20.2.0/fmriprep/sub-' num2str(sub) '/ses-1/func/'];
    file = ['sub-' num2str(sub) '_ses-1_task-film_run-1_space-fsnative_hemi-L_bold.func.gii'];
    
    mri_file = [base file];
    gifti_path = gifti(mri_file);
    gifti_data = gifti_path.cdata;
    dmdt_data = demean_detrend(gifti_data);
    dmdt_regressed_data = regress_nuisance(dmdt_data);

    % filter
    lopasscutoff=.08;
    hipasscutoff=.009;
    [butta buttb]=butter(1,[hipasscutoff lopasscutoff]);
    clean_gifti=filtfilt(butta,buttb,double(dmdt_regressed_data));

    save(gifti(clean_gifti),['sub-' num2str(sub) '.func.gii'],'Base64Binary');
end 

function [tempbold tempbetas] = demean_detrend(img)
    [tempbold]=img;
    [vox ts]=size(tempbold);    
    tmask=ones(ts,1);
    linreg=[repmat(1,[ts 1]) linspace(0,1,ts)'];
    tempboldcell=num2cell(tempbold(:,logical(tmask))',1);
    linregcell=repmat({linreg(logical(tmask),:)},[1 vox]);
    tempbetas = cellfun(@mldivide,linregcell,tempboldcell,'uniformoutput',0);
    tempbetas=cell2mat(tempbetas);
    tempbetas=tempbetas';
    tempintvals=tempbetas*linreg';
    tempbold=tempbold-tempintvals;
end

function [tempimg zb newregs] = regress_nuisance(tempimg)

    [vox ts]=size(tempimg);
    tot_tmask=ones(ts,1);
    
    conf_names = {'csf','white_matter','global_signal', 'trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z'};
    confounds_file = '/projects/b1081/member_directories/zladwig/neurohackademy/Nifti/derivatives/preproc_fmriprep-20.2.0/fmriprep/sub-22/ses-1/func/sub-22_ses-1_task-film_run-1_desc-confounds_timeseries.tsv';
    nuisance = tdfread(confounds_file);
    totregs = [];
    
    for i = 1:length(conf_names)
        conf = conf_names{i};
        b = nuisance.(conf);
        totregs(:,i) = nuisance.(conf);
    end
    
    zlinreg=totregs(logical(tot_tmask),:); % only desired data
    [zlinreg DMDTB]=demean_detrend(zlinreg'); % obtain fits for desired data
    zlinreg=zlinreg';
    zstd=std(zlinreg); % calculate std
    zmean=mean(zlinreg);
    zlinreg=(zlinreg-repmat(zmean,[size(zlinreg,1) 1]))./(repmat(zstd,[size(zlinreg,1) 1])); % zscore
    
    linreg=[repmat(1,[ts 1]) linspace(0,1,ts)'];
    newregs=DMDTB*linreg'; % predicted all regressors demean/detrend
    newregs=totregs-newregs'; % these are the demeaned detrended regressors
    newregs=(newregs-repmat(zmean,[size(newregs,1) 1]))./(repmat(zstd,[size(newregs,1) 1])); % zscore
    
    % now we have z-scored, detrended good and all regressors.
    
    % demean and detrend the desired data
    zmdtimg=tempimg(:,logical(tot_tmask));
    [zmdtimg zmdtbetas]=demean_detrend(zmdtimg);
    
    % calculate betas on the good data
    tempboldcell=num2cell(zmdtimg',1);
    zlinregcell=repmat({zlinreg},[1 vox]);
    zb = cellfun(@mldivide,zlinregcell,tempboldcell,'uniformoutput',0);
    zb=cell2mat(zb);
    
    % demean and detrend all data using good fits
    [zmdttotimg]=zmdtbetas*linreg';
    zmdttotimg=tempimg-zmdttotimg;
    
    % calculate residuals on all the data
    zb=zb';
    tempintvals=zb*newregs';
    tempimg=zmdttotimg-tempintvals;
end
