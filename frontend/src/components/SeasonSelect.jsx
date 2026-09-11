import styles from './SeasonSelect.module.css'

export default function SeasonSelect({ seasons, value, onChange }) {
  return (
    <div className={styles.wrap}>
      <label className={styles.label}>Season</label>
      <div className={styles.selectWrap}>
        <select
          className={styles.select}
          value={value}
          onChange={e => onChange(e.target.value)}
        >
          {seasons.map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
        <svg className={styles.chevron} width="11" height="11" viewBox="0 0 12 12" fill="none">
          <path d="M2 4l4 4 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </div>
    </div>
  )
}
