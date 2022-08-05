clear all;
subjects = [14, 16, 18, 22, 27, 41, 45, 46, 55, 60];
for i = 1:length(subjects)
    % load processed data
    sub = subjects(i);

    fcproc_data = ['fcproc_giftis/sub-' num2str(sub) '.func.gii'];
    gifti_path = gifti(fcproc_data);
    clean_gifti = gifti_path.cdata;

    % get the ROIs
    roi_file = ['roi_labels/sub-' num2str(sub) '_ALL_5mm-radius.txt'];
    t = readtable(roi_file,'ReadVariableNames',false);
    t.Properties.VariableNames = ["vertex", "name"];
    electrodes = unique(t.name);
    
    % map the ROI
    roi = [];
    for i = 1:length(electrodes)
        idx = find(strcmp(t.name, electrodes{i}));
        bold = mean(clean_gifti(idx,:));
        roi(i,:) = bold;
    end
    
    % save out the file
    roi_corr = corr(roi');
    save(['corrmats/sub-' num2str(sub) '-fmri.mat'], 'roi_corr', 'electrodes')
    imagesc(roi_corr)
end
