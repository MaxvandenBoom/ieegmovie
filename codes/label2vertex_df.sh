project_dir=/Users/bramdiamond/Desktop/iEEG_project
subj=sub-22
deriv_dir=${project_dir}/derivatives/
coord_csv=$project_dir/$subj/ses-iemu/ieeg/${subj}_ses-iemu_acq-clinical_electrodes.tsv
export SUBJECTS_DIR=${project_dir}/derivatives/freesurfer

IFS=$'\n'

vertex_df=$project_dir/$subj/ses-iemu/ieeg/${subj}_ses-iemu_acq-clinical_electrodes_surface_labels_fsnative.txt

echo "" > $vertex_df

for coord in $(tail -n +2 $project_dir/$subj/ses-iemu/ieeg/${subj}_ses-iemu_acq-clinical_electrodes.tsv); do

	electrode_name=$(echo $coord | awk '{ print $1}')
	coords=$(echo $coord | awk '{ print $2 " " $3 " " $4}')
	x_coord=$(echo $coords | awk '{ print $1 }')
	y_coord=$(echo $coords | awk '{ print $2 }')
	z_coord=$(echo $coords | awk '{ print $3 }')

	label_f=$deriv_dir/freesurfer/$subj/label/${subj}_${electrode_name}_5mm-radius.label

	for line in $(tail -n +3 $label_f); do 

		vertex=$(echo $line | awk '{ print $1 }')
		
		echo $vertex $electrode_name

	done

done