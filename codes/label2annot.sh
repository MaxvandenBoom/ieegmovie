# turn labels into annotation

project_dir=/Users/bramdiamond/Desktop/iEEG_project
deriv_dir=${project_dir}/derivatives/
export SUBJECTS_DIR=${project_dir}/derivatives/freesurfer

IFS=$'\n'

annot_cmd_file=${project_dir}/scripts/annot_cmd.sh

touch $annot_cmd_file

for subj in $(ls $deriv_dir/freesurfer | grep sub-); do

	coord_csv=$project_dir/$subj/ses-iemu/ieeg/${subj}_ses-iemu_acq-clinical_electrodes.tsv

	label_cmd=""

	for coord in $(tail -n +2 $coord_csv); do 

		electrode_name=$(echo $coord | awk '{ print $1}')
		coords=$(echo $coord | awk '{ print $2 " " $3 " " $4}')
		x_coord=$(echo $coords | awk '{ print $1 }')
		y_coord=$(echo $coords | awk '{ print $2 }')
		z_coord=$(echo $coords | awk '{ print $3 }')

		vertext_num=$(echo $coord | awk '{ print $(NF) }')

		label_cmd="--l ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_5mm-radius.label ${label_cmd}"

	done

	echo "mris_label2annot --s $subj --h lh $label_cmd --annot-path ${project_dir}/derivatives/freesurfer/$subj/label/electrodes.annot --ctab $FREESURFER_HOME/FreeSurferColorLUT.txt" >> $annot_cmd_file

done

bash $annot_cmd_file