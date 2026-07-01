import styles from './ChartPanel.module.css'

export default function ChartPanel({ data, loading, slot }) {
  return (
    <div className={`${styles.panel} ${styles[`panel-${slot}`]}`}>
      {loading && (
        <div className={styles.loader}>
          <div className={`${styles.spinner} ${styles[`spinner-${slot}`]}`} />
          <span>Loading chart…</span>
        </div>
      )}
      {!loading && data?.svg && (
        <div
          className={styles.svgWrap}
          dangerouslySetInnerHTML={{ __html: data.svg }}
        />
      )}
      {!loading && !data && (
        <div className={styles.empty}>Select a player above</div>
      )}
    </div>
  )
}
