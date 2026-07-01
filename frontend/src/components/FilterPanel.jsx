import RangeSlider from './RangeSlider.jsx'
import styles from './FilterPanel.module.css'

function inchesLabel(n) {
  return `${Math.floor(n / 12)}'${n % 12}"`
}

function activeCount(f, d) {
  let n = 0
  if (f.height[0] > d.height[0] || f.height[1] < d.height[1]) n++
  if (f.weight[0] > d.weight[0] || f.weight[1] < d.weight[1]) n++
  if (f.positions.length > 0)                                   n++
  if (f.exp[0]    > d.exp[0]    || f.exp[1]    < d.exp[1])    n++
  if (f.draft[0]  > d.draft[0]  || f.draft[1]  < d.draft[1])  n++
  if (!f.includeUndrafted)                                      n++
  return n
}

const POSITIONS = ['G', 'F', 'C']

export default function FilterPanel({ open, onToggle, filters, onChange, defaults }) {
  const count = activeCount(filters, defaults)

  function set(key, val) { onChange({ ...filters, [key]: val }) }

  function togglePos(pos) {
    const next = filters.positions.includes(pos)
      ? filters.positions.filter(p => p !== pos)
      : [...filters.positions, pos]
    set('positions', next)
  }

  return (
    <div className={styles.wrap}>
      <div className={styles.toggleRow}>
        <button
          className={`${styles.toggle} ${open ? styles.toggleOpen : ''}`}
          onClick={onToggle}
        >
          <svg width="13" height="13" viewBox="0 0 16 16" fill="none">
            <path d="M2 4h12M4 8h8M6 12h4" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round"/>
          </svg>
          Filters
          {count > 0 && <span className={styles.badge}>{count}</span>}
        </button>
        {count > 0 && (
          <button className={styles.clearInline} onClick={() => onChange({ ...defaults })}>
            Clear all
          </button>
        )}
      </div>

      {open && (
        <div className={styles.panel}>
          <div className={styles.grid}>

            <div className={styles.row}>
              <label className={styles.label}>Height</label>
              <RangeSlider
                min={defaults.height[0]} max={defaults.height[1]}
                value={filters.height}
                onChange={v => set('height', v)}
                format={inchesLabel}
              />
            </div>

            <div className={styles.row}>
              <label className={styles.label}>Weight (lbs)</label>
              <RangeSlider
                min={defaults.weight[0]} max={defaults.weight[1]}
                value={filters.weight}
                onChange={v => set('weight', v)}
                format={v => `${v}`}
              />
            </div>

            <div className={styles.row}>
              <label className={styles.label}>Position</label>
              <div className={styles.chips}>
                {POSITIONS.map(pos => (
                  <button
                    key={pos}
                    className={`${styles.chip} ${filters.positions.includes(pos) ? styles.chipOn : ''}`}
                    onClick={() => togglePos(pos)}
                  >
                    {pos}
                  </button>
                ))}
                {filters.positions.length > 0 && (
                  <span className={styles.posHint}>incl. combos</span>
                )}
              </div>
            </div>

            <div className={styles.row}>
              <label className={styles.label}>Experience (yrs)</label>
              <RangeSlider
                min={defaults.exp[0]} max={defaults.exp[1]}
                value={filters.exp}
                onChange={v => set('exp', v)}
                format={v => `${v}`}
              />
            </div>

            <div className={styles.row}>
              <label className={styles.label}>Draft Pick</label>
              <RangeSlider
                min={defaults.draft[0]} max={defaults.draft[1]}
                value={filters.draft}
                onChange={v => set('draft', v)}
                format={v => `#${v}`}
              />
              <label className={styles.checkLabel}>
                <input
                  type="checkbox"
                  className={styles.check}
                  checked={filters.includeUndrafted}
                  onChange={e => set('includeUndrafted', e.target.checked)}
                />
                Include undrafted
              </label>
            </div>

          </div>

          <div className={styles.footer}>
            <button className={styles.clearAll} onClick={() => onChange({ ...defaults })}>
              Reset filters
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
