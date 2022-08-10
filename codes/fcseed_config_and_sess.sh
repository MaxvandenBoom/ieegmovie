# create fcseed-config and fcseed-sess for electrodes, then make correlation matrix

project_dir=/Users/bramdiamond/Desktop/iEEG_project
deriv_dir=${project_dir}/derivatives/
export SUBJECTS_DIR=${project_dir}/derivatives/freesurfer

IFS=$'\n'

for subj in sub-22; do #$(ls $deriv_dir/freesurfer | grep sub-); do

	fcseedcor_cmd=${project_dir}/scripts/${subj}_fcseedcor_cmd.sh

	rm $fcseedcor_cmd
	echo "fcseedcor \ " >> $fcseedcor_cmd
	echo "-s ${subj} -fsd film \c" >> $fcseedcor_cmd

	for coord in $(tail -n +2 $project_dir/$subj/ses-iemu/ieeg/${subj}_ses-iemu_acq-clinical_electrodes.tsv); do

		electrode_name=$(echo $coord | awk '{ print $1}')

		label_f=$deriv_dir/freesurfer/$subj/label/${subj}_${electrode_name}_5mm-radius.label

		if [ ! -e $deriv_dir/freesurfer/$subj/mri/${subj}_${electrode_name}_5mm-radius.label.mgz ]; then

			mri_label2vol \
				--o $deriv_dir/freesurfer/$subj/mri/${subj}_${electrode_name}_5mm-radius.label.mgz \
				--label $label_f \
				--identity \
				--fill-ribbon \
				--subject $subj \
				--hemi lh \
				--surf pial

		fi

		mkdir -p $deriv_dir/freesurfer/electrode_config_files

		if [ ! -e $deriv_dir/freesurfer/electrode_config_files/${subj}_${electrode_name}_5mm-radius.config ]; then
		
			fcseed-config \
				-seg ${label_f}.mgz \
				-segid 1 \
				-fcname ${subj}_${electrode_name}_5mm-radius.dat \
				-fsd film \
				-mean \
				-cfg $deriv_dir/freesurfer/electrode_config_files/${subj}_${electrode_name}_5mm-radius.config
		
		fi

		if [ ! -e $deriv_dir/freesurfer/$subj/film/001/${subj}_${electrode_name}_5mm-radius.dat ]; then

			fcseed-sess \
				-s $subj \
				-cfg $deriv_dir/freesurfer/electrode_config_files/${subj}_${electrode_name}_5mm-radius.config

		fi

		echo "${subj}_${electrode_name}_5mm-radius.dat / " >> $fcseedcor_cmd

	done

	echo " -xreg global.waveform.dat 1 \ " >> $fcseedcor_cmd
	echo " -xreg vcsf.dat 1 \ " >> $fcseedcor_cmd
	echo " -xreg wm.dat 1 \ " >> $fcseedcor_cmd
	echo " -xreg mcprextreg 6 \ " >> $fcseedcor_cmd
	echo " -hpf .01 -lpf .2 -nskip 4 \ " >> $fcseedcor_cmd
	echo " -o seedcor.dat " >> $fcseedcor_cmd

done

bash $fcseed-config







