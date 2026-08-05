import styles from './SimilarPlayers.module.css'

function SimilarityBar({ score }) {
  return (
    <div className={styles.barTrack}>
      <div className={styles.barFill} style={{ width: `${Math.round(score * 100)}%` }} />
    </div>
  )
}

function SimilarList({ data, slot }) {
  if (!data?.similar?.length) return (
    <div className={styles.empty}>Run precompute.py to enable similarity</div>
  )

  return (
    <div className={`${styles.list} ${styles[`list-${slot}`]}`}>
      {data.similar.map((p, i) => (
        <div key={p.id} className={styles.row}>
          <span className={styles.rank}>{i + 1}</span>
          <span className={styles.name}>{p.name}</span>
          <SimilarityBar score={p.score} />
          <span className={styles.score}>{Math.round(p.score * 100)}%</span>
        </div>
      ))}
    </div>
  )
}

export default function SimilarPlayers({ dataA, dataB }) {
  if (!dataA && !dataB) return null

  return (
    <div className={styles.wrap}>
      <h3 className={styles.heading}>Most Similar Shot Profiles</h3>
      <div className={styles.cols}>
        <div className={styles.col}>
          {dataA?.name && <p className={styles.colLabel}>{dataA.name}</p>}
          <SimilarList data={dataA} slot="a" />
        </div>
        <div className={styles.col}>
          {dataB?.name && <p className={styles.colLabel}>{dataB.name}</p>}
          <SimilarList data={dataB} slot="b" />
        </div>
      </div>
    </div>
  )
}
