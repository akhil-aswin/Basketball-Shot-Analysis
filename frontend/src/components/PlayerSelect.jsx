import { useState, useEffect, useRef, useMemo } from 'react'
import styles from './PlayerSelect.module.css'

function playerLabel(p) {
  if (!p) return ''
  const tag = p.dnp ? 'Did Not Play' : p.height ? p.height.replace('-', "'") : ''
  return tag ? `${p.name}  ·  ${tag}` : p.name
}

export default function PlayerSelect({ players, selected, onChange, label, slot }) {
  const [open, setOpen]   = useState(false)
  const [query, setQuery] = useState('')
  const wrapRef           = useRef(null)
  const inputRef          = useRef(null)

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return players
    return players.filter(p => p.name.toLowerCase().includes(q))
  }, [players, query])

  useEffect(() => {
    if (open) {
      setQuery('')
      setTimeout(() => inputRef.current?.focus(), 0)
    }
  }, [open])

  // Close on outside click
  useEffect(() => {
    if (!open) return
    function handle(e) {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', handle)
    return () => document.removeEventListener('mousedown', handle)
  }, [open])

  function pick(player) {
    onChange(player)
    setOpen(false)
  }

  return (
    <div ref={wrapRef} className={`${styles.wrap} ${styles[`slot-${slot}`]}`}>
      <label className={styles.label}>{label}</label>

      <button
        className={`${styles.trigger} ${open ? styles.triggerOpen : ''}`}
        onClick={() => setOpen(o => !o)}
      >
        <span className={styles.triggerText}>
          {selected ? playerLabel(selected) : 'Select a player…'}
        </span>
        <svg
          className={`${styles.chevron} ${open ? styles.chevronUp : ''}`}
          width="12" height="12" viewBox="0 0 12 12" fill="none"
        >
          <path d="M2 4l4 4 4-4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>

      {open && (
        <div className={styles.panel}>
          <div className={styles.searchWrap}>
            <svg className={styles.searchIcon} width="13" height="13" viewBox="0 0 16 16" fill="none">
              <circle cx="6.5" cy="6.5" r="4.5" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M10 10l3 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            <input
              ref={inputRef}
              className={styles.search}
              placeholder="Search players…"
              value={query}
              onChange={e => setQuery(e.target.value)}
            />
            {query && (
              <button className={styles.clearSearch} onClick={() => setQuery('')}>✕</button>
            )}
          </div>

          <ul className={styles.list}>
            {filtered.length === 0 && (
              <li className={styles.empty}>No players match "{query}"</li>
            )}
            {filtered.map(p => (
              <li
                key={p.id}
                className={`${styles.item} ${selected?.id === p.id ? styles.itemSelected : ''} ${p.dnp ? styles.itemDnp : ''}`}
                onClick={() => pick(p)}
              >
                <span className={styles.itemName}>{p.name}</span>
                {p.dnp
                  ? <span className={styles.dnpTag}>DNP</span>
                  : p.height
                    ? <span className={styles.heightTag}>{p.height.replace('-', "'")}</span>
                    : null
                }
              </li>
            ))}
          </ul>

          <div className={styles.listFooter}>
            {filtered.length} player{filtered.length !== 1 ? 's' : ''}
          </div>
        </div>
      )}
    </div>
  )
}
