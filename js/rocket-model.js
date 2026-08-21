(() => {
    "use strict";

    // -----------------------------
    // Media placeholders
    // -----------------------------
    document.querySelectorAll("[data-video-placeholder]").forEach((figure) => {
        const video = figure.querySelector("video");
        const frame = figure.querySelector(".rocket-video-frame");
        if (!video || !frame) return;

        const markReady = () => frame.classList.add("is-ready");
        video.addEventListener("loadedmetadata", markReady, { once: true });
        video.addEventListener("canplay", markReady, { once: true });
    });

    // -----------------------------
    // Interactive reconstruction of
    // preliminary_calculations.m
    // -----------------------------
    const canvas = document.getElementById("rocket-regression-chart");
    if (!canvas) return;

    const portInput = document.getElementById("rocket-port-input");
    const burnInput = document.getElementById("rocket-burn-input");
    const portOutput = document.getElementById("rocket-port-output");
    const burnOutput = document.getElementById("rocket-burn-output");
    const finalPort = document.getElementById("rocket-final-port");
    const finalWeb = document.getElementById("rocket-final-web");
    const reset = document.getElementById("rocket-model-reset");

    const project = {
        thrust: 600,
        isp: 260,
        ofRatio: 7,
        gravity: 9.81,
        grainLength: 0.3,
        regressionA: 0.0001,
        regressionN: 0.6,
        regressionM: 0,
        fuelDensity: 950,
        outerGrainDiameter: 0.1,
        dt: 0.1,
        initialPortMm: 20,
        burnSeconds: 5
    };

    function simulate(initialPortMm, burnSeconds) {
        // Same regression logic used in preliminary_calculations.m.
        const totalMassFlow = project.thrust / (project.isp * project.gravity);
        const propellantMass = totalMassFlow * burnSeconds;
        const fuelMass = propellantMass / (1 + project.ofRatio);
        const oxidiserMassFlow = project.ofRatio * (fuelMass / burnSeconds);

        let diameter = initialPortMm / 1000;
        let t = 0;
        const rows = [];

        while (t <= burnSeconds + 1e-9) {
            const web = (project.outerGrainDiameter - diameter) / 2;
            rows.push({
                time: t,
                portMm: diameter * 1000,
                webMm: web * 1000
            });

            if (diameter >= project.outerGrainDiameter || t >= burnSeconds) break;

            const oxidiserFlux = (4 * oxidiserMassFlow) / (Math.PI * diameter * diameter);
            const regressionRate =
                project.regressionA *
                Math.pow(oxidiserFlux, project.regressionN) *
                Math.pow(project.grainLength, project.regressionM);

            diameter = diameter + 2 * regressionRate * project.dt;
            t = Math.min(burnSeconds, t + project.dt);
        }

        return rows;
    }

    function cssVar(name, fallback) {
        const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
        return value || fallback;
    }

    function draw(rows) {
        const rect = canvas.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;
        canvas.width = Math.max(1, Math.floor(rect.width * dpr));
        canvas.height = Math.max(1, Math.floor(rect.height * dpr));

        const ctx = canvas.getContext("2d");
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

        const w = rect.width;
        const h = rect.height;
        const pad = { left: 58, right: 24, top: 28, bottom: 48 };
        const pw = w - pad.left - pad.right;
        const ph = h - pad.top - pad.bottom;

        const bg = cssVar("--surface", "#fff");
        const text = cssVar("--text", "#171717");
        const muted = cssVar("--muted", "#626262");
        const border = cssVar("--border", "#d8d8d3");
        const accent = cssVar("--accent", "#173f5f");

        ctx.clearRect(0, 0, w, h);
        ctx.fillStyle = bg;
        ctx.fillRect(0, 0, w, h);

        const xMax = Math.max(...rows.map(r => r.time), 1);
        const yMaxRaw = Math.max(...rows.flatMap(r => [r.portMm, r.webMm]));
        const yMax = Math.ceil(yMaxRaw / 10) * 10;

        const x = v => pad.left + (v / xMax) * pw;
        const y = v => pad.top + ph - (v / yMax) * ph;

        ctx.font = "12px Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif";
        ctx.lineWidth = 1;

        // Grid + labels
        ctx.strokeStyle = border;
        ctx.fillStyle = muted;
        for (let i = 0; i <= 5; i++) {
            const xv = (xMax / 5) * i;
            const xp = x(xv);
            ctx.beginPath();
            ctx.moveTo(xp, pad.top);
            ctx.lineTo(xp, pad.top + ph);
            ctx.stroke();
            ctx.textAlign = "center";
            ctx.fillText(xv.toFixed(xMax % 1 ? 1 : 0), xp, h - 20);
        }

        for (let i = 0; i <= 5; i++) {
            const yv = (yMax / 5) * i;
            const yp = y(yv);
            ctx.beginPath();
            ctx.moveTo(pad.left, yp);
            ctx.lineTo(pad.left + pw, yp);
            ctx.stroke();
            ctx.textAlign = "right";
            ctx.fillText(yv.toFixed(0), pad.left - 10, yp + 4);
        }

        ctx.fillStyle = text;
        ctx.textAlign = "center";
        ctx.fillText("Time (s)", pad.left + pw / 2, h - 3);

        ctx.save();
        ctx.translate(15, pad.top + ph / 2);
        ctx.rotate(-Math.PI / 2);
        ctx.fillText("Geometry (mm)", 0, 0);
        ctx.restore();

        function series(key, stroke, dashed = false) {
            ctx.save();
            ctx.strokeStyle = stroke;
            ctx.lineWidth = 2.2;
            ctx.setLineDash(dashed ? [7, 5] : []);
            ctx.beginPath();
            rows.forEach((row, i) => {
                const xp = x(row.time);
                const yp = y(row[key]);
                if (i === 0) ctx.moveTo(xp, yp);
                else ctx.lineTo(xp, yp);
            });
            ctx.stroke();
            ctx.restore();
        }

        series("portMm", accent, false);
        series("webMm", text, true);

        // Legend
        ctx.font = "12px Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif";
        ctx.textAlign = "left";
        const ly = 13;

        ctx.strokeStyle = accent;
        ctx.lineWidth = 2.2;
        ctx.setLineDash([]);
        ctx.beginPath();
        ctx.moveTo(pad.left, ly);
        ctx.lineTo(pad.left + 24, ly);
        ctx.stroke();
        ctx.fillStyle = text;
        ctx.fillText("Port diameter", pad.left + 32, ly + 4);

        ctx.strokeStyle = text;
        ctx.setLineDash([7, 5]);
        ctx.beginPath();
        ctx.moveTo(pad.left + 145, ly);
        ctx.lineTo(pad.left + 169, ly);
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillText("Web thickness", pad.left + 177, ly + 4);
    }

    function update() {
        const initialPortMm = Number(portInput.value);
        const burnSeconds = Number(burnInput.value);

        portOutput.value = `${initialPortMm.toFixed(0)} mm`;
        burnOutput.value = `${burnSeconds.toFixed(burnSeconds % 1 ? 1 : 0)} s`;

        const rows = simulate(initialPortMm, burnSeconds);
        const last = rows[rows.length - 1];

        finalPort.textContent = `${last.portMm.toFixed(1)} mm`;
        finalWeb.textContent = `${last.webMm.toFixed(1)} mm`;

        draw(rows);
    }

    portInput.addEventListener("input", update);
    burnInput.addEventListener("input", update);
    reset.addEventListener("click", () => {
        portInput.value = project.initialPortMm;
        burnInput.value = project.burnSeconds;
        update();
    });

    let resizeTimer;
    window.addEventListener("resize", () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(update, 80);
    });

    update();
})();
