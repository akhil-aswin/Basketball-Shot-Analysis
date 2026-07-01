import HeroSection from './HeroSection.jsx'
import ChartPanel from './ChartPanel.jsx'
import StatBarRow from './StatBarRow.jsx'
import styles from './CompareCard.module.css'

function barWidths(a, b, maxPx = 56) {
  if (!a || !b) return [maxPx, maxPx]
  const max = Math.max(a, b, 0.0001)
  return [Math.round((a / max) * maxPx), Math.round((b / max) * maxPx)]
}

export default function CompareCard({ dataA, dataB, loadingA, loadingB }) {
  const ready = dataA && dataB

  const fgWA  = ready ? barWidths(dataA.stats.fg, dataB.stats.fg) : [0, 0]
  const tpWA  = ready ? barWidths(dataA.stats['3p'], dataB.stats['3p']) : [0, 0]
  const volWA = ready ? barWidths(dataA.stats.fga, dataB.stats.fga) : [0, 0]
  const pppWA = ready ? barWidths(dataA.stats.ppp, dataB.stats.ppp) : [0, 0]

  return (
    <div className={styles.card}>
      <HeroSection dataA={dataA} dataB={dataB} />

      <div className={styles.chartsArea}>
        <ChartPanel data={dataA} loading={loadingA} slot="a" />
        <ChartPanel data={dataB} loading={loadingB} slot="b" />
      </div>

      {ready && (
        <div className={styles.statsGrid}>
          <StatBarRow
            label="FG%"
            valA={`${dataA.stats.fg.toFixed(1)}%`}
            valB={`${dataB.stats.fg.toFixed(1)}%`}
            barA={fgWA[0]} barB={fgWA[1]}
          />
          <StatBarRow
            label="3PT%"
            valA={`${dataA.stats['3p'].toFixed(1)}%`}
            valB={`${dataB.stats['3p'].toFixed(1)}%`}
            barA={tpWA[0]} barB={tpWA[1]}
          />
          <StatBarRow
            label="Volume"
            valA={String(dataA.stats.fga)}
            valB={String(dataB.stats.fga)}
            barA={volWA[0]} barB={volWA[1]}
          />
          <StatBarRow
            label="PPP"
            valA={dataA.stats.ppp.toFixed(3)}
            valB={dataB.stats.ppp.toFixed(3)}
            barA={pppWA[0]} barB={pppWA[1]}
          />
        </div>
      )}
    </div>
  )
}
