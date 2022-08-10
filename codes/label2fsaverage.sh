# move label to fsaverage, make heatmap

project_dir=/Users/bramdiamond/Desktop/iEEG_project
deriv_dir=${project_dir}/derivatives/
export SUBJECTS_DIR=${project_dir}/derivatives/freesurfer

IFS=$'\n'

annot_cmd_file2=${project_dir}/scripts/annot_cmd2.sh

touch $annot_cmd_file2

for subj in $(ls $deriv_dir/freesurfer | grep sub-); do

	for coord in $(tail -n +2 $project_dir/$subj/ses-iemu/ieeg/${subj}_ses-iemu_acq-clinical_electrodes.tsv); do

		electrode_name=$(echo $coord | awk '{ print $1}')
		coords=$(echo $coord | awk '{ print $2 " " $3 " " $4}')
		x_coord=$(echo $coords | awk '{ print $1 }')
		y_coord=$(echo $coords | awk '{ print $2 }')
		z_coord=$(echo $coords | awk '{ print $3 }')

		label_in=$deriv_dir/freesurfer/$subj/label/${subj}_${electrode_name}_5mm-radius.label

		label_out=$deriv_dir/freesurfer/$subj/label/${subj}_${electrode_name}_5mm-radius_fsaverage.label

		mri_label2label \
			--srcsubject $subj \
			--srclabel $label_in \
			--trgsubject fsaverage \
			--trglabel $label_out \
			--regmethod surface \
			--hemi lh

		label_cmd="--l $label_out ${label_cmd}"

	done

done

echo "mris_label2annot --s fsaverage --h lh $label_cmd --annot-path ${project_dir}/derivatives/freesurfer/all_electrodes.annot --ctab $FREESURFER_HOME/FreeSurferColorLUT.txt --nhits ${project_dir}/derivatives/freesurfer/all_electrodes_heatmap.mgz" >> $annot_cmd_file2

bash $annot_cmd_file2

