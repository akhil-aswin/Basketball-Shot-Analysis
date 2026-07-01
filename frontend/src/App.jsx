import { useState, useEffect, useCallback, useMemo } from 'react'
import PlayerSelect from './components/PlayerSelect.jsx'
import CompareCard from './components/CompareCard.jsx'
import FilterPanel from './components/FilterPanel.jsx'
import styles from './App.module.css'

function makeBounds(players) {
  const heights = players.map(p => p.height_in).filter(Boolean)
  const weights = players.map(p => p.weight).filter(Boolean)
  const exps    = players.map(p => p.exp).filter(v => v != null)
  return {
    height: [Math.min(...heights), Math.max(...heights)],
    weight: [Math.min(...weights), Math.max(...weights)],
    positions: [],
    exp:    [0, Math.max(...exps)],
    draft:  [1, 60],
    includeUndrafted: true,
  }
}

export default function App() {
  const [players, setPlayers]       = useState([])
  const [filterOpen, setFilterOpen] = useState(false)
  const [filters, setFilters]       = useState(null)
  const [selA, setSelA]             = useState(null)
  const [selB, setSelB]             = useState(null)
  const [dataA, setDataA]           = useState(null)
  const [dataB, setDataB]           = useState(null)
  const [loadingA, setLoadingA]     = useState(false)
  const [loadingB, setLoadingB]     = useState(false)

  useEffect(() => {
    fetch('/api/players')
      .then(r => r.json())
      .then(list => {
        setPlayers(list)
        setFilters(makeBounds(list))
        if (list.length >= 2) { setSelA(list[0]); setSelB(list[1]) }
      })
  }, [])

  const defaults = useMemo(() => players.length ? makeBounds(players) : null, [players])

  const filtered = useMemo(() => {
    if (!filters || !defaults) return players

    const heightActive = filters.height[0] > defaults.height[0] || filters.height[1] < defaults.height[1]
    const weightActive = filters.weight[0] > defaults.weight[0] || filters.weight[1] < defaults.weight[1]
    const expActive    = filters.exp[0]    > defaults.exp[0]    || filters.exp[1]    < defaults.exp[1]
    const draftActive  = filters.draft[0]  > defaults.draft[0]  || filters.draft[1]  < defaults.draft[1]

    return players.filter(p => {
      // When a filter is active, players missing that field are excluded
      if (heightActive && (p.height_in == null || p.height_in < filters.height[0] || p.height_in > filters.height[1])) return false
      if (weightActive && (p.weight    == null || p.weight    < filters.weight[0] || p.weight    > filters.weight[1])) return false
      if (expActive    && (p.exp       == null || p.exp       < filters.exp[0]    || p.exp       > filters.exp[1]))    return false
      if (filters.positions.length > 0) {
        if (!filters.positions.some(f => (p.position ?? '').includes(f))) return false
      }
      if (p.draft_pick != null) {
        if (draftActive && (p.draft_pick < filters.draft[0] || p.draft_pick > filters.draft[1])) return false
      } else {
        if (!filters.includeUndrafted) return false
      }
      return true
    })
  }, [players, filters, defaults])

  useEffect(() => {
    if (!filtered.length) return
    if (selA && !filtered.find(p => p.id === selA.id)) setSelA(filtered[0])
    if (selB && !filtered.find(p => p.id === selB.id)) setSelB(filtered[filtered.length > 1 ? 1 : 0])
  }, [filtered])

  const fetchShots = useCallback((player, slot, setData, setLoading) => {
    if (!player) return
    setLoading(true)
    setData(null)
    fetch(`/api/shots/${player.id}?slot=${slot}`)
      .then(r => r.json())
      .then(d => setData({ ...d, name: player.name }))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => { fetchShots(selA, 'a', setDataA, setLoadingA) }, [selA, fetchShots])
  useEffect(() => { fetchShots(selB, 'b', setDataB, setLoadingB) }, [selB, fetchShots])

  return (
    <div className={styles.app}>
      <div className={styles.header}>
        <h1 className={styles.title}>NBA Shot Chart</h1>
        <p className={styles.season}>2025–26 Regular Season</p>

        {filters && defaults && (
          <FilterPanel
            open={filterOpen}
            onToggle={() => setFilterOpen(o => !o)}
            filters={filters}
            onChange={setFilters}
            defaults={defaults}
          />
        )}
      </div>

      <div className={styles.selectors}>
        <PlayerSelect players={filtered} selected={selA} onChange={setSelA} label="Player 1" slot="a" />
        <PlayerSelect players={filtered} selected={selB} onChange={setSelB} label="Player 2" slot="b" />
      </div>

      <CompareCard dataA={dataA} dataB={dataB} loadingA={loadingA} loadingB={loadingB} />
    </div>
  )
}
