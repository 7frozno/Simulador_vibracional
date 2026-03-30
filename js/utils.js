/**
 * Utilidades para análisis de señales vibratorias
 */

// ===== FFT Implementation =====
class FFT {
    static fft(signal) {
        const N = signal.length;
        if (N === 1) return signal;

        if (N % 2 !== 0) {
            throw new Error("FFT requires signal length to be power of 2");
        }

        const even = FFT.fft(signal.filter((_, i) => i % 2 === 0));
        const odd = FFT.fft(signal.filter((_, i) => i % 2 === 1));

        const result = new Array(N);
        for (let k = 0; k < N / 2; k++) {
            const t = complexMultiply(
                { real: Math.cos(-2 * Math.PI * k / N), imag: Math.sin(-2 * Math.PI * k / N) },
                odd[k]
            );
            result[k] = complexAdd(even[k], t);
            result[k + N / 2] = complexSubtract(even[k], t);
        }
        return result;
    }

    static magnitude(complexArray) {
        return complexArray.map(c => Math.sqrt(c.real ** 2 + c.imag ** 2));
    }

    static fftForSignal(signal) {
        // Preparar señal (padding a potencia de 2)
        let paddedSignal = signal.slice();
        const n = Math.pow(2, Math.ceil(Math.log2(signal.length)));
        while (paddedSignal.length < n) {
            paddedSignal.push(0);
        }

        // Convertir a números complejos
        const complexSignal = paddedSignal.map(x => ({ real: x, imag: 0 }));

        // Aplicar FFT
        const fftResult = FFT.fft(complexSignal);

        // Obtener magnitudes
        return FFT.magnitude(fftResult);
    }
}

// ===== Complex Number Operations =====
function complexAdd(a, b) {
    return {
        real: a.real + b.real,
        imag: a.imag + b.imag
    };
}

function complexSubtract(a, b) {
    return {
        real: a.real - b.real,
        imag: a.imag - b.imag
    };
}

function complexMultiply(a, b) {
    return {
        real: a.real * b.real - a.imag * b.imag,
        imag: a.real * b.imag + a.imag * b.real
    };
}

// ===== Signal Analysis Functions =====
class SignalAnalyzer {
    static calculateRMS(signal) {
        if (signal.length === 0) return 0;
        const meanSquare = signal.reduce((sum, val) => sum + val * val, 0) / signal.length;
        return Math.sqrt(meanSquare);
    }

    static calculatePeak(signal) {
        return Math.max(...signal.map(x => Math.abs(x)));
    }

    static calculatePeakToPeak(signal) {
        const min = Math.min(...signal);
        const max = Math.max(...signal);
        return max - min;
    }

    static calculateCrestFactor(signal) {
        const peak = SignalAnalyzer.calculatePeak(signal);
        const rms = SignalAnalyzer.calculateRMS(signal);
        return rms > 0 ? peak / rms : 0;
    }

    static calculateKurtosis(signal) {
        if (signal.length === 0) return 0;

        const mean = signal.reduce((a, b) => a + b, 0) / signal.length;
        const variance = signal.reduce((sum, x) => sum + Math.pow(x - mean, 2), 0) / signal.length;
        const std = Math.sqrt(variance);

        if (std === 0) return 3;

        const fourthMoment = signal.reduce((sum, x) => sum + Math.pow((x - mean) / std, 4), 0) / signal.length;
        return fourthMoment;
    }

    static calculateSkewness(signal) {
        if (signal.length === 0) return 0;

        const mean = signal.reduce((a, b) => a + b, 0) / signal.length;
        const variance = signal.reduce((sum, x) => sum + Math.pow(x - mean, 2), 0) / signal.length;
        const std = Math.sqrt(variance);

        if (std === 0) return 0;

        const thirdMoment = signal.reduce((sum, x) => sum + Math.pow((x - mean) / std, 3), 0) / signal.length;
        return thirdMoment;
    }

    static getFrequencyComponents(signal, samplingRate, rpm) {
        const fftMagnitude = FFT.fftForSignal(signal);
        const n = fftMagnitude.length;
        const freqs = Array.from({ length: n }, (_, i) => i * samplingRate / n);

        const f0 = rpm / 60.0; // Fundamental frequency

        const features = {};
        for (let harmonic = 1; harmonic <= 7; harmonic++) {
            const targetFreq = harmonic * f0;
            const idx = Math.round(targetFreq / (samplingRate / n));
            features[`${harmonic}X_amplitude`] = idx < fftMagnitude.length ? fftMagnitude[idx] : 0;
        }

        return { frequencies: freqs, magnitudes: fftMagnitude, features };
    }

    static getAllFeatures(signal, samplingRate, rpm) {
        const freq = SignalAnalyzer.getFrequencyComponents(signal, samplingRate, rpm);

        return {
            time_domain: {
                rms: SignalAnalyzer.calculateRMS(signal),
                peak: SignalAnalyzer.calculatePeak(signal),
                peak_to_peak: SignalAnalyzer.calculatePeakToPeak(signal),
                crest_factor: SignalAnalyzer.calculateCrestFactor(signal),
                kurtosis: SignalAnalyzer.calculateKurtosis(signal),
                skewness: SignalAnalyzer.calculateSkewness(signal),
                mean: signal.reduce((a, b) => a + b, 0) / signal.length,
                std: Math.sqrt(signal.reduce((sum, x) => sum + Math.pow(x - signal.reduce((a, b) => a + b, 0) / signal.length, 2), 0) / signal.length)
            },
            frequency_domain: freq.features,
            frequencies: freq.frequencies,
            magnitudes: freq.magnitudes
        };
    }
}

// ===== Filter Functions =====
class SignalFilters {
    static normalize(signal, method = 'minmax') {
        if (method === 'minmax') {
            const min = Math.min(...signal);
            const max = Math.max(...signal);
            if (max === min) return signal;
            return signal.map(x => (x - min) / (max - min));
        } else if (method === 'zscore') {
            const mean = signal.reduce((a, b) => a + b, 0) / signal.length;
            const std = Math.sqrt(signal.reduce((sum, x) => sum + Math.pow(x - mean, 2), 0) / signal.length);
            if (std === 0) return signal;
            return signal.map(x => (x - mean) / std);
        }
        return signal;
    }

    static applyWindow(signal, windowType = 'hann') {
        const n = signal.length;
        let window;

        if (windowType === 'hann') {
            window = Array.from({ length: n }, (_, i) => 0.5 * (1 - Math.cos(2 * Math.PI * i / (n - 1))));
        } else if (windowType === 'hamming') {
            window = Array.from({ length: n }, (_, i) => 0.54 - 0.46 * Math.cos(2 * Math.PI * i / (n - 1)));
        } else {
            window = Array(n).fill(1);
        }

        return signal.map((x, i) => x * window[i]);
    }
}

// ===== Utility Functions =====
function linspace(start, end, num) {
    const step = (end - start) / (num - 1);
    return Array.from({ length: num }, (_, i) => start + i * step);
}

function randomNormal(mean = 0, std = 1) {
    let u = 0, v = 0;
    while (u === 0) u = Math.random();
    while (v === 0) v = Math.random();
    const z = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    return z * std + mean;
}

function getEnergyInBands(magnitudes, freqs, fs) {
    const lowBand = magnitudes.filter((_, i) => freqs[i] > 0 && freqs[i] < 500);
    const midBand = magnitudes.filter((_, i) => freqs[i] >= 500 && freqs[i] < 2000);
    const highBand = magnitudes.filter((_, i) => freqs[i] >= 2000);

    return {
        low_freq_energy: lowBand.reduce((a, b) => a + b * b, 0),
        mid_freq_energy: midBand.reduce((a, b) => a + b * b, 0),
        high_freq_energy: highBand.reduce((a, b) => a + b * b, 0)
    };
}
