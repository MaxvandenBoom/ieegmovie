# make 5 mm radius sphere at iEEG electrode coord

project_dir=/Users/bramdiamond/Desktop/iEEG_project
deriv_dir=${project_dir}/derivatives/
export SUBJECTS_DIR=${project_dir}/derivatives/freesurfer

IFS=$'\n'

for subj in sub-60; do #$(ls $deriv_dir/freesurfer | grep sub-); do

	coord_csv=$project_dir/$subj/ses-iemu/ieeg/${subj}_ses-iemu_acq-clinical_electrodes.tsv

	for coord in $(tail -n +2 $coord_csv); do 

		electrode_name=$(echo $coord | awk '{ print $1}')
		coords=$(echo $coord | awk '{ print $2 " " $3 " " $4}')
		x_coord=$(echo $coords | awk '{ print $1 }')
		y_coord=$(echo $coords | awk '{ print $2 }')
		z_coord=$(echo $coords | awk '{ print $3 }')

		vertext_num=$(echo $coord | awk '{ print $(NF) }')

		echo "working on subject $subj: $electrode_name"

		# label_cmd="--l ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_5mm-radius.label ${label_cmd}"

		if [ ! -e ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_5mm-radius.label ]; then

			# On Surface ##

			 mri_volsynth \
				--template ${project_dir}/derivatives/freesurfer/$subj/surf/lh.thickness \
				--pdf delta \
				--delta-crsf $vertext_num 0 0 0 \
				--o ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_delta.mgz

			mris_fwhm \
				--so \
				--niters 6 \
				--i ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_delta.mgz \
				--o ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_delta.5mm-radius.mgz \
				--s $subj \
				--hemi lh

			mri_binarize \
				--i ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_delta.5mm-radius.mgz \
				--min 0.00001 \
				--o ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_5mm-radius.mgz

			mri_vol2label \
				--i ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_5mm-radius.mgz \
				--l ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_5mm-radius.label \
				--surf $subj lh \
				--id 1

			# Fill GM

			# mri_surf2vol \
			# 	--surfval ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_5mm-radius.mgz \
			# 	--o ${project_dir}/derivatives/freesurfer/$subj/mri/${subj}_${electrode_name}_5mm-radius_vol.mgz \
			# 	--subject $subj \
			# 	--fillribbon \
			# 	--hemi lh \
			# 	--template ${project_dir}/derivatives/freesurfer/$subj/mri/aseg.mgz \
			# 	--identity $subj

		fi

		rm ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_delta.mgz ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_delta.5mm-radius.mgz ${project_dir}/derivatives/freesurfer/$subj/label/${subj}_${electrode_name}_5mm-radius.mgz

	done

done