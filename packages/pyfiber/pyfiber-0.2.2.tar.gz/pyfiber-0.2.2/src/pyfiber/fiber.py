import numpy as np
import pandas as pd
import random
import time
import scipy.signal as signal
import matplotlib.pyplot as plt
import os
from typing import List, Tuple, Union, Any
import matplotlib.style as st
st.use('ggplot')

from ._utils import PyFiber as PyFiber
__all__ = ['Fiber']

Intervals = List[Tuple[float,float]]
Events = np.ndarray

class Fiber(PyFiber):
    """Extract and analyse fiberphotometry data.

    :param filepath:
    :type filepath: str
    :param name: 
    :type name: str
    :param ID:
    :type ID: hashable"""
    vars().update(PyFiber.FIBER)

    def __init__(self,
                 filepath :str,
                 name='default',
                 ID=None,
                 alignement=0,
                 filetype=None,
                 **kwargs):
        start = time.time()
        super().__init__(**kwargs)
        
        self.alignement = alignement
        self.filepath = filepath
        self._print(f'Importing {filepath}...')
        self.ID = ID
        
        if name == 'default':
            self.name = self.filepath.split('/')[-1].split('.csv')[0]
            if self.ID:
                self.name += ID
        self.number_of_recording = 0
        
        if filetype:
            self.ncl = self.SYSTEM[filetype.upper()]
        else:
            self.ncl = self.SYSTEM['DORIC']

        self.df = self._read_file(filepath, alignement=alignement)
        self.full_time = np.array(self.df[ [k for k,v in self.ncl.items() if v == 'time'][0] ])
        self.raw_columns = list(self.df.columns)
        self.data = self._extract_data()
        self.columns = list(self.data.columns)
        
        if self.split_recordings:
            self.recordings = self._split_recordings()
        else:
            self.recordings = {1: self.data}
        
        self.rec_length = np.array(
            [v.time.to_numpy()[-1]-v.time.to_numpy()[0] for k, v in self.recordings.items()])
        self.sampling_rate = np.mean(
            [len(df)/t for df, t in zip(self.recordings.values(), self.rec_length)])
        self.rec_intervals = [tuple([self.recordings[recording]['time'].values[index] for index in [
                                    0, -1]]) for recording in range(1, self.number_of_recording+1)]
        
        self.peaks = {}
        self._print('Analyzing peaks...')
        for r in self.recordings.keys():
            data = self.norm(rec=r, add_time=True)
            t = data[:, 0]
            s = data[:, 1]
            self.peaks[r] = self._detect_peaks(t, s, plot=False)
        
        self._print(
            f'Importing of {filepath} finished in {time.time() - start} seconds')

    def __repr__(self):
        """Give general information about the recording data."""
        general_info = f"""\
File                     : {self.filepath}
ID                       : {self.ID}
Number of recordings     : {self.number_of_recording}
Data columns             : {self.columns}
Total span               : {self.full_time[-1] - self.full_time[0]} s
Recording lengths        : {self.rec_length} ({self.trim_recording} seconds trimmed from each)
Global sampling rate     : {self.sampling_rate} S/s
Aligned to behavior file : {self.alignement} s
"""
        return general_info

    def _find_rec(self, timestamp):
        """Find recording number corresponding to inputed timestamp."""
        rec_num = self.number_of_recording
        time_nom = 'time'
        return [i for i in range(1, rec_num+1) if self.get(time_nom, recording=i)[0] <= timestamp <= self.get(time_nom, recording=i)[-1]]


    def _read_file(self, filepath, alignement=0):
        """Read file and align the timestamps if specified"""
        df = pd.read_csv(filepath, usecols=[k for k,v in self.ncl.items() if v in ['signal','control','time']], dtype=np.float64)  # ,engine='pyarrow')
        time_nom = [k for k,v in self.ncl.items() if v == 'time'][0]
        df[time_nom] = df[time_nom] + alignement
        return df

    def _extract_data(self):
        """Extract raw fiber data from Doric system."""
        return pd.DataFrame({self.ncl[i]: self.df[i].to_numpy() for i in self.ncl if i in self.raw_columns})

    def _split_recordings(self):
        """Cut at timestamp jumps (defined by a step greater than N times the mean sample space (defined in config.yaml)."""
        time = self.full_time
        jumps = list(
            np.where(np.diff(time) > self.split_treshold * np.mean(np.diff(time)))[0] + 1)
        indices = [0] + jumps + [len(time)-1]
        ind_tuples = [(indices[i], indices[i+1]) for i in range(len(indices)-1)
                      if indices[i+1]-indices[i] > self.min_sample_per_rec]
        self.number_of_recording = len(ind_tuples)
        self._print(f"Found {self.number_of_recording} separate recordings.")
        rec = {ind_tuples.index(
            (s, e))+1: self.data.iloc[s:e, :] for s, e in ind_tuples}
        t_ = 'time'
        rec = {k: v[v[t_] > v[t_].to_numpy()[0]+self.trim_recording]
               for k, v in rec.items()}
        return rec

    def plot(self,
             which='all',
             method='default',
             figsize=(20,20),
             raw_label=['Ca-dependant','isosbestic'],
             norm_label='Normalized signal',
             xlabel='Time (s)',
             ylabel_raw='Signal (mV)',
             ylabel_norm='Signal (%)',
             title='Recording',
             hspace=0.5
             ):
        """Hey I'm here!"""
        if which == 'all':
            recs = list(self.recordings.keys())
        else:
            recs = self._list(which)
        data = [self.norm(rec=i, method=method, add_time=True) for i in recs]
        rawdata = [self.norm(rec=i, method='raw', add_time=True) for i in recs]
        n = len(recs)
        plt.figure(figsize=figsize)
        for i in range(n):
            plt.subplot(n, 2, int(i*2)+1)
            plt.plot(rawdata[i][:,0], rawdata[i][:,1:], label = raw_label)
            plt.legend()
            plt.xlabel(xlabel)
            plt.ylabel(ylabel_raw)
            plt.title(title+f' ({i+1})')
            
            plt.subplot(n, 2, int(2*(i+1)))
            plt.plot(data[i][:,0], data[i][:,1], c='g', label=norm_label+f' ({method})')
            plt.legend()
            plt.xlabel(xlabel)
            plt.ylabel(ylabel_norm)
            plt.title(title+f' ({i+1})')
        plt.subplots_adjust(hspace = hspace)

    def to_csv(self,
               recordings='all',
               auto=True,
               columns=None,
               column_names=None,
               prefix='default'):
        """Export data to csv.

        - recording     (integer/list/'all') : default behaviour is exporting all recordings (if multiple splitted recordings exist); alternatively a single or a few splits can be chosen
        - auto          (True/False)         : automatically export signal and isosbestic separately with sampling_rate
        - columns       ([<names>])          : (changes auto to False) export specific columns with their timestamps (columns names accessible with <obj>.columns
        - columns_names ([<names>])          : change default name for columns in outputted csv (the list must correspond to the column list)
        - prefix        ('string']           : default prefix is 'raw filename + recording number' (followed by data column name)
        """
        if prefix == 'default':
            prefix = self.name
        if recordings == 'all':
            recordings = list(self.recordings.keys())
        sig_nom = "signal"
        ctrl_nom = "control"
        time_nom = "time"
        if auto and not columns:
            nomenclature = {sig_nom: 'signal', ctrl_nom: 'control'}
            for rec in recordings:
                time = self.get(time_nom, rec)
                for dataname in nomenclature.keys():
                    df = pd.DataFrame({'timestamps': time,
                                       'data': self.get(dataname, rec),
                                       'sampling_rate': [1/np.diff(time)] + [np.nan]*(len(time)-1)})  # timestamps data sampling rate
                    df.to_csv(os.path.join(Fiber.FOLDER,
                                           f'{prefix}_{rec}_{nomenclature[dataname]}.csv'), index=False)
        else:
            recordings = self._list(recordings)
            columns = self._list(columns)
            column_names = self._list(column_names)
            for r in recordings:
                time = self.get(time_nom, r)
                for c in columns:
                    df = pd.DataFrame({'timestamps': time,
                                       'data': self.get(c, r),
                                       'sampling_rate': [1/np.diff(time)] + [np.nan]*(len(time)-1)})
                    df.to_csv(f'{prefix}_{r}_{c}.csv', index=False)


    def get(self,
            column,
            recording=1,
            add_time=False,
            as_df=False):
        """Extracts a data array from a specific column of a recording (default is first recording)
        - add_time (False) : if True returns a 2D array with time included
        - as_df    (False) : if True returns data as a data frame (add_time will automatically set to True)"""
        time_nom = 'time'
        data = np.array(self.recordings[recording][column])
        time = np.array(self.recordings[recording][time_nom])
        if as_df:
            return pd.DataFrame({time_nom: time, column: data})
        if add_time:
            return np.vstack((time, data)).T
        else:
            return data

    # def TTL(self, ttl, rec=1):
    #     """Output TTL timestamps."""
    #     ttl = self.get(f"TTL{ttl}", rec)
    #     time = self.get('time', rec)
    #     ttl[ttl < 0.01] = 0
    #     ttl[ttl >= 0.01] = 1
    #     if (ttl == 1).all():
    #         return [time[0]]
    #     if (ttl == 0).all():
    #         return []
    #     index = np.where(np.diff(ttl) == 1)[0]
    #     return [time[i] for i in index]

    def norm(self,
             rec=1,
             method='default',
             add_time=True):
        """Normalize data with specified method"""
        sig = self.get("signal", rec)
        ctrl = self.get("control", rec)
        tm = self.get("time", rec)
        if method == 'default':
            method = self.default_norm
        self._print(f"Normalizing recording {rec} with method '{method}'")
        if method == 'F':
            coeff = np.polynomial.polynomial.polyfit(ctrl, sig, 1)
            #fitted_control = np.polynomial.polynomial.polyval(coeff,ctrl)
            # coeff = np.polyfit(ctrl,sig,1) /!\ coeff order is inversed with np.polyfit vs np.p*.p*.polyfit
            fitted_control = coeff[0] + ctrl*coeff[1]
            normalized = (sig - fitted_control)/fitted_control
        if method == 'Z':
            S = (sig - sig.mean())/signal.std()
            I = (ctrl - ctrl.mean())/ctrl.std()
            normalized = S-I
        if method == 'raw' or not method:
            normalized = np.vstack((sig, ctrl))
        if add_time:
            return np.vstack((tm, normalized)).T
        else:
            return normalized

    def _detect_peaks(self, t, s, window='default', distance='default', plot=True, figsize=(30, 10), zscore='full', bMAD='default', pMAD='default'):
        """Detect peaks on segments of data:

        window:   window size for peak detection, the median is calculated for each bin
        distance: minimun distance between peaks, limits peak over detection
        zscore:   full if zscore is to be computed on the whole recording before splitting in bins, or bins if after
        plot,figsize: parameters for plotting
        """
        if window == 'default':
            window = self.peak_window
        if distance == 'default':
            distance = self.peak_distance
        if zscore == 'default':
            zscore = self.peak_zscore
        if bMAD == 'default':
            bMAD = int(self.peak_baseline_MAD)
        else:
            bMAD = int(bMAD)
        if pMAD == 'default':
            pMAD = int(self.peak_peak_MAD)
        else:
            pMAD = int(pMAD)
        dF = s
        # calculate zscores
        if zscore == 'full':
            s = (s - s.mean())/s.std()
        # distance
        distance = round(float(distance.split(
            'ms')[0])/(np.mean(np.diff(t))*1000))
        if distance == 0:
            distance = 1
        # find indexes for n second windows
        t_points = np.arange(t[0], t[-1], window)
        if t_points[-1] != t[-1]:
            t_points = np.concatenate((t_points, [t[-1]]))
        indexes = [np.where(abs(t-i) == abs(t-i).min())[0][0]
                   for i in t_points]
        # create time bins
        bins = [pd.Series(s[indexes[i-1]:indexes[i]], index=t[indexes[i-1]:indexes[i]])
                for i in range(1, len(indexes))]
        dFbins = [pd.Series(dF[indexes[i-1]:indexes[i]], index=t[indexes[i-1]:indexes[i]])
                  for i in range(1, len(indexes))]
        if zscore == 'bins':
            bins = [(b - b.mean())/b.std() for b in bins]
        # find median for each bin and remove events >2MAD for baselines
        baselines = [
            b[b < np.median(b) + bMAD*np.median(abs(b - np.median(b)))] for b in bins]
        # calculate peak tresholds for each bin, by default >3MAD of previsoult created baseline
        tresholds = [np.median(b)+pMAD*np.median(abs(b-np.median(b)))
                     for b in baselines]
        # find peaks using scipy.signal.find_peaks with thresholds
        peaks = []
        for n, bin_ in enumerate(bins):
            b = pd.DataFrame(bin_).reset_index()
            indices, heights = signal.find_peaks(
                b.iloc[:, 1], height=tresholds[n], distance=distance)
            peaks.append(pd.DataFrame({'time': [b.iloc[i, 0] for i in indices],
                                       'dF/F': [dFbins[n].iloc[i] for i in indices],
                                       'zscore': list(heights.values())[0]}))
        if plot:
            plt.figure(figsize=figsize)
            peak_tresholds = [pd.Series(t, index=baselines[n].index)
                              for n, t in enumerate(tresholds)]
            bin_medians = [pd.Series(np.median(b), index=bins[n].index)
                           for n, b in enumerate(bins)]
            bin_mad = [pd.Series(np.median(
                abs(b - np.median(b))), index=bins[n].index) for n, b in enumerate(bins)]
            for n, i in enumerate(bins):
                c = random.choice(list('bgrcmy'))
                plt.plot(i, alpha=0.6, color=c)
                plt.plot(baselines[n], color=c, label=n *
                         '_'+'signal <2MAD + median')
                plt.plot(bin_medians[n], color='k',
                         label=n*'_'+'signal median')
                plt.plot(bin_medians[n]+bin_mad[n]*2,
                         color='darkgray', label=n*'_'+'>2MAD + median')
                plt.plot(peak_tresholds[n], color='r',
                         label=n*'_'+'>3MAD + baseline')
            for n, p in enumerate(peaks):
                plt.scatter(p.loc[:, 'time'], p.loc[:, 'zscore'])
            plt.legend()
        return pd.concat(peaks, ignore_index=True)

    def plot_transients(self, value='zscore', figsize=(20, 20), rec='all', colors='k', alpha=0.3, **kwargs):
        """Show graphical representation of detected transients with their amplitude."""
        if rec == 'all':
            rec = self.number_of_recording
        fig, axes = plt.subplots(rec, figsize=figsize)
        if type(axes) != np.ndarray:
            axes.grid(which='both')
            data = self.peaks[1]
            for i in data.index:
                axes.vlines(data.loc[i, 'time'],
                            ymin=0, ymax=data.loc[i, value],
                            colors=colors, alpha=alpha, **kwargs)
        else:
            for n, ax in enumerate(axes):
                ax.grid(which='both')
                data = self.peaks[n+1]
                for i in data.index:
                    ax.vlines(data.loc[i, 'time'],
                              ymin=0, ymax=data.loc[i, value],
                              colors=colors, alpha=alpha, **kwargs)
        plt.show()

    def peakFA(self, a, b):
        r = 0
        for n, i in enumerate(self.rec_intervals):
            if (i[0] <= a < i[1]) and (i[0] < b <= i[1]):
                r = n+1
        if r == 0:
            return
        data = self.peaks[r][(self.peaks[r]['time'] > a)
                             & (self.peaks[r]['time'] < b)]
        return {'frequency': len(data)/(b-a),
                'mean zscore': data['zscore'].mean(),
                'mean dF/F': data['dF/F'].mean(),
                'max zscore': data['zscore'].max(),
                'max dF/F': data['dF/F'].max(),
                'data': data}
