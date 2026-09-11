import styles from './HeightFilter.module.css'

function inchesToLabel(inches) {
  const ft  = Math.floor(inches / 12)
  const inn = inches % 12
  return `${ft}'${inn}"`
}

export default function HeightFilter({ minHeight, onChange, min = 66, max = 90 }) {
  return (
    <div className={styles.wrap}>
      <span className={styles.label}>Min Height</span>
      <input
        type="range"
        className={styles.slider}
        min={min}
        max={max}
        value={minHeight}
        onChange={e => onChange(Number(e.target.value))}
      />
      <span className={styles.value}>{inchesToLabel(minHeight)}</span>
      {minHeight > min && (
        <button className={styles.reset} onClick={() => onChange(min)}>✕</button>
      )}
    </div>
  )
}
