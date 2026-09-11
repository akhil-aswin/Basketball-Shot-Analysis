import styles from './RangeSlider.module.css'

export default function RangeSlider({ min, max, value, onChange, format = v => v }) {
  const [lo, hi] = value
  const pctLo = ((lo - min) / (max - min)) * 100
  const pctHi = ((hi - min) / (max - min)) * 100

  const trackStyle = {
    background: `linear-gradient(to right,
      rgba(255,255,255,0.07) ${pctLo}%,
      var(--color-a) ${pctLo}%,
      var(--color-a) ${pctHi}%,
      rgba(255,255,255,0.07) ${pctHi}%)`
  }

  return (
    <div className={styles.wrap}>
      <div className={styles.sliderContainer}>
        <div className={styles.track} style={trackStyle} />
        <input
          type="range" className={styles.input}
          min={min} max={max} value={lo}
          onChange={e => onChange([Math.min(Number(e.target.value), hi - 1), hi])}
        />
        <input
          type="range" className={styles.input}
          min={min} max={max} value={hi}
          onChange={e => onChange([lo, Math.max(Number(e.target.value), lo + 1)])}
        />
      </div>
      <div className={styles.labels}>
        <span className={styles.val}>{format(lo)}</span>
        <span className={styles.val}>{format(hi)}</span>
      </div>
    </div>
  )
}
