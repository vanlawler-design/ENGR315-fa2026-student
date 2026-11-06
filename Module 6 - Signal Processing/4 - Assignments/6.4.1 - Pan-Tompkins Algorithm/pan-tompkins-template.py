from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfiltfilt, find_peaks
from scipy.ndimage import uniform_filter1d
from ekg_testbench import EKGTestBench

def detect_heartbeats(filepath):
    """
    Perform analysis to detect location of heartbeats
    :param filepath: A valid path to a CSV file of heart beats
    :return: signal: a signal that will be plotted
    beats: the indices of detected heartbeats
    """
    if filepath == '':
        raise ValueError("Please provide a CSV filepath.")

    # import the CSV file using numpy
    path = filepath

    # load data in matrix from CSV file; skip first two rows
    ## your code here
    data = np.loadtxt(path, delimiter=',', skiprows=2)

    # save each vector as own variable
    ## your code here
    time = data[:, 0]
    signal = data[:, 1]  # MLII ECG measurements; column 0 contains time.
    sampling_rate = (len(time) - 1) / (time[-1] - time[0])

    # identify one column to process. Call that column signal

    # Band-pass filtering removes baseline drift and high-frequency noise.
    # Use the sampling rate so the cutoff frequencies are in Hz.
    sos = butter(3, [5, 18], btype='bandpass', fs=sampling_rate, output='sos')
    bandpass_signal = sosfiltfilt(sos, signal)

    # Differentiate and square to emphasize the rapid changes in each beat.
    differentiated_signal = np.diff(bandpass_signal, prepend=bandpass_signal[0])
    squared_signal = differentiated_signal ** 2

    # Average over 120 ms, preserving the original sample indices.
    averaged_signal = uniform_filter1d(
        squared_signal, size=max(1, round(0.12 * sampling_rate))
    )

    # Adapt the threshold to the surrounding three seconds. A global maximum
    # can be dominated by a noise spike and cause most beats to be missed.
    local_energy = uniform_filter1d(
        averaged_signal, size=max(1, round(3.0 * sampling_rate))
    )
    peaks, _ = find_peaks(
        averaged_signal,
        distance=max(1, int(0.28 * sampling_rate)),
        height=0.7 * local_energy,
    )

    # Return the processed signal for plotting alongside the detected indices.
    signal = averaged_signal
    beats = peaks

    # do not modify this line
    return signal, beats


# when running this file directly, this will execute first
if __name__ == "__main__":

    # place here so doesn't cause import error
    import matplotlib.pyplot as plt

    # database name
    database_name = 'mitdb_201'

    # set to true if you wish to generate a debug file
    file_debug = False

    # set to true if you wish to print overall stats to the screen
    print_debug = True

    # set to true if you wish to show a plot of each detection process
    show_plot = False

    ### DO NOT MODIFY BELOW THIS LINE!!! ###

    # path to ekg folder
    path_to_folder = str(Path(__file__).resolve().parents[3] / "data" / "ekg") + "/"

    # select a signal file to run
    signal_filepath = path_to_folder + database_name + ".csv"

    # call main() and run against the file. Should return the filtered
    # signal and identified peaks
    (signal, peaks) = detect_heartbeats(signal_filepath)

    # stop with a clear message if detect_heartbeats() is not finished yet
    if peaks is None:
        raise SystemExit("detect_heartbeats() returned None for beats. Finish the steps above and return the peak indices.")

    # matched is a list of (peak, annotation) pairs; unmatched is a list of peaks that were
    # not matched to any annotation; and remaining is annotations that were not matched.
    annotation_path = path_to_folder + database_name + "_annotations.txt"
    tb = EKGTestBench(annotation_path)
    peaks_list = peaks.tolist()
    (matched, unmatched, remaining) = tb.generate_stats(peaks_list)

    # if was matched, then is true positive
    true_positive = len(matched)

    # if response was unmatched, then is false positive
    false_positive = len(unmatched)

    # whatever remains in annotations is a missed detection
    false_negative = len(remaining)

    # calculate f1 score
    f1 = true_positive / (true_positive + 0.5 * (false_positive + false_negative))

    # if we wish to show the resulting plot
    if show_plot:
        # make a nice plt of results
        plt.title('Signal for ' + database_name + " with detections")

        plt.plot(signal, label="Filtered Signal")
        plt.plot(peaks, signal[peaks], 'p', label='Detected Peaks')

        true_annotations = np.asarray(tb.annotation_indices)
        plt.plot(true_annotations, signal[true_annotations], 'o', label='True Annotations')

        plt.legend()

        # uncomment line to show the plot
        plt.show()

    # if we wish to save all the stats to a file
    if file_debug:
        # print out more complex stats to the debug file
        debug_file_path = database_name + "_debug_stats.txt"
        debug_file = open(debug_file_path, 'w')

        # print out indices of all false positives
        debug_file.writelines("-----False Positives Indices-----\n")
        for fp in unmatched:
            debug_file.writelines(str(fp) + "\n")

        # print out indices of all false negatives
        debug_file.writelines("-----False Negatives Indices-----\n")
        for fn in remaining:
            debug_file.writelines(str(fn.sample) + "\n")

        # close file that we writing
        debug_file.close()

    if print_debug:
        print("-------------------------------------------------")
        print("Database|\t\tTP|\t\tFP|\t\tFN|\t\tF1")
        print(database_name, "|\t\t", true_positive, "|\t", false_positive, '|\t', false_negative, '|\t', round(f1, 3))
        print("-------------------------------------------------")

    print("Done!")
