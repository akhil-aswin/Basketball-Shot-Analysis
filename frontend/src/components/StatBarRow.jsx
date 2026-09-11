import styles from './StatBarRow.module.css'

export default function StatBarRow({ label, valA, valB, barA, barB }) {
  return (
    <div className={styles.cell}>
      <p className={styles.label}>{label}</p>
      <div className={styles.row}>
        <span className={`${styles.val} ${styles.valA}`}>{valA}</span>
        <div className={styles.bars}>
          <div className={styles.barTrack}>
            <div className={`${styles.bar} ${styles.barA}`} style={{ width: barA }} />
          </div>
          <div className={styles.barTrack}>
            <div className={`${styles.bar} ${styles.barB}`} style={{ width: barB }} />
          </div>
        </div>
        <span className={`${styles.val} ${styles.valB}`}>{valB}</span>
      </div>
    </div>
  )
}
