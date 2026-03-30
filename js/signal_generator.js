/**
 * Generador de señales vibratorias sintéticas
 */

class SignalConfig {
    constructor(samplingRate = 10000, duration = 1.0, rpm = 1500, amplitude = 1.0) {
        this.sampling_rate = samplingRate;
        this.duration = duration;
        this.rpm = rpm;
        this.amplitude = amplitude;
        this.f0 = rpm / 60.0; // Fundamental frequency
    }
}

class SignalGenerator {
    constructor(config = null) {
        this.config = config || new SignalConfig();
        this.time = null;
        this.signal = null;
    }

    generateHealthy() {
        const fs = this.config.sampling_rate;
        const duration = this.config.duration;
        const n = Math.floor(fs * duration);

        this.time = linspace(0, duration, n);

        // Ruido blanco base
        let signal = Array.from({ length: n }, () => randomNormal(0, this.config.amplitude * 0.1));

        const f0 = this.config.f0;

        // 1X - Velocidad sincrónica
        for (let i = 0; i < n; i++) {
            signal[i] += this.config.amplitude * 0.05 * Math.sin(2 * Math.PI * f0 * this.time[i]);
        }

        // 2X
        for (let i = 0; i < n; i++) {
            signal[i] += this.config.amplitude * 0.03 * Math.sin(2 * Math.PI * 2 * f0 * this.time[i]);
        }

        // Ruido de fluido
        for (let i = 0; i < n; i++) {
            signal[i] += this.config.amplitude * 0.08 * Math.sin(2 * Math.PI * 50 * this.time[i]);
        }

        this.signal = signal;
        return { time: this.time, signal: signal };
    }

    generateBeatingFault(beatFreq = 20) {
        const fs = this.config.sampling_rate;
        const duration = this.config.duration;
        const n = Math.floor(fs * duration);

        this.time = linspace(0, duration, n);
        const signal = new Array(n);

        const f0 = this.config.f0;
        const carrierFreq = 2000;

        for (let i = 0; i < n; i++) {
            const t = this.time[i];

            // Modulación AM
            const modulation = 0.5 * (1 + Math.sin(2 * Math.PI * beatFreq * t));

            // Portadora
            const carrier = this.config.amplitude * 0.8 * Math.sin(
                2 * Math.PI * carrierFreq * t +
                0.3 * Math.cos(2 * Math.PI * beatFreq * t)
            );

            signal[i] = modulation * carrier;
            signal[i] += this.config.amplitude * 0.1 * Math.sin(2 * Math.PI * f0 * t);
            signal[i] += this.config.amplitude * 0.05 * Math.sin(2 * Math.PI * 2 * f0 * t);
            signal[i] += randomNormal(0, this.config.amplitude * 0.05);
        }

        this.signal = signal;
        return { time: this.time, signal: signal };
    }

    generateCavitation() {
        const fs = this.config.sampling_rate;
        const duration = this.config.duration;
        const n = Math.floor(fs * duration);

        this.time = linspace(0, duration, n);
        let signal = Array.from({ length: n }, () => randomNormal(0, this.config.amplitude * 0.6));

        const f0 = this.config.f0;
        const impulseFreq = 5 * f0;

        for (let t = 0; t < duration; t += 1 / impulseFreq) {
            for (let i = 0; i < n; i++) {
                const impulseWindow = Math.exp(-Math.pow(this.time[i] - t, 2) / Math.pow(0.001, 2));
                signal[i] += this.config.amplitude * 0.7 * impulseWindow *
                    Math.sin(2 * Math.PI * 3000 * (this.time[i] - t));
            }
        }

        for (let i = 0; i < n; i++) {
            signal[i] += this.config.amplitude * 0.15 * Math.sin(2 * Math.PI * f0 * this.time[i]);
        }

        this.signal = signal;
        return { time: this.time, signal: signal };
    }

    generateMisalignment(severity = 1.0) {
        const fs = this.config.sampling_rate;
        const duration = this.config.duration;
        const n = Math.floor(fs * duration);

        this.time = linspace(0, duration, n);
        let signal = Array.from({ length: n }, () => randomNormal(0, this.config.amplitude * 0.1));

        const f0 = this.config.f0;
        const amplitudes = [0.15, 0.25, 0.18, 0.22, 0.12, 0.15];

        for (let harmonic = 1; harmonic <= 6; harmonic++) {
            const amp = amplitudes[harmonic - 1];
            for (let i = 0; i < n; i++) {
                signal[i] += this.config.amplitude * amp * severity *
                    Math.sin(2 * Math.PI * harmonic * f0 * this.time[i]);
            }
        }

        this.signal = signal;
        return { time: this.time, signal: signal };
    }

    generateUnbalance(severity = 1.0) {
        const fs = this.config.sampling_rate;
        const duration = this.config.duration;
        const n = Math.floor(fs * duration);

        this.time = linspace(0, duration, n);
        let signal = Array.from({ length: n }, () => randomNormal(0, this.config.amplitude * 0.1));

        const f0 = this.config.f0;

        // 1X dominante
        for (let i = 0; i < n; i++) {
            signal[i] += this.config.amplitude * 0.6 * severity * Math.sin(2 * Math.PI * f0 * this.time[i]);
        }

        // 2X y 3X menores
        for (let i = 0; i < n; i++) {
            signal[i] += this.config.amplitude * 0.05 * Math.sin(2 * Math.PI * 2 * f0 * this.time[i]);
            signal[i] += this.config.amplitude * 0.08 * Math.sin(2 * Math.PI * 3 * f0 * this.time[i]);
        }

        for (let n_harm = 4; n_harm <= 6; n_harm++) {
            for (let i = 0; i < n; i++) {
                signal[i] += this.config.amplitude * 0.03 * Math.sin(2 * Math.PI * n_harm * f0 * this.time[i]);
            }
        }

        this.signal = signal;
        return { time: this.time, signal: signal };
    }

    generateWithNoise(baseSignal, snrDb = 30) {
        const signalPower = baseSignal.reduce((sum, x) => sum + x * x, 0) / baseSignal.length;
        const noisePower = signalPower / Math.pow(10, snrDb / 10);

        return baseSignal.map(x => x + randomNormal(0, Math.sqrt(noisePower)));
    }
}
