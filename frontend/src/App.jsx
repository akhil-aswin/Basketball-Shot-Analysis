import { useState, useEffect, useCallback, useMemo } from 'react'
import PlayerSelect from './components/PlayerSelect.jsx'
import CompareCard from './components/CompareCard.jsx'
import FilterPanel from './components/FilterPanel.jsx'
import SeasonSelect from './components/SeasonSelect.jsx'
import styles from './App.module.css'

function makeBounds(players) {
  const heights = players.map(p => p.height_in).filter(Boolean)
  const weights = players.map(p => p.weight).filter(Boolean)
  const exps    = players.map(p => p.exp).filter(v => v != null)
  if (!heights.length || !weights.length || !exps.length) return null
  const archetypeOptions = [...new Set(players.map(p => p.archetype).filter(Boolean))].sort()
  return {
    height: [Math.min(...heights), Math.max(...heights)],
    weight: [Math.min(...weights), Math.max(...weights)],
    positions: [],
    archetypes: [],
    archetypeOptions,
    exp:   [0, Math.max(...exps)],
    draft: [1, 60],
    includeUndrafted: true,
  }
}

function applyFilters(players, filters, defaults) {
  if (!filters || !defaults) return players
  const heightActive = filters.height[0] > defaults.height[0] || filters.height[1] < defaults.height[1]
  const weightActive = filters.weight[0] > defaults.weight[0] || filters.weight[1] < defaults.weight[1]
  const expActive    = filters.exp[0]    > defaults.exp[0]    || filters.exp[1]    < defaults.exp[1]
  const draftActive  = filters.draft[0]  > defaults.draft[0]  || filters.draft[1]  < defaults.draft[1]

  return players.filter(p => {
    if (heightActive && (p.height_in == null || p.height_in < filters.height[0] || p.height_in > filters.height[1])) return false
    if (weightActive && (p.weight    == null || p.weight    < filters.weight[0] || p.weight    > filters.weight[1])) return false
    if (expActive    && (p.exp       == null || p.exp       < filters.exp[0]    || p.exp       > filters.exp[1]))    return false
    if (filters.positions.length > 0) {
      if (!filters.positions.some(f => (p.position ?? '').includes(f))) return false
    }
    if (filters.archetypes.length > 0) {
      if (!filters.archetypes.includes(p.archetype)) return false
    }
    if (p.draft_pick != null) {
      if (draftActive && (p.draft_pick < filters.draft[0] || p.draft_pick > filters.draft[1])) return false
    } else {
      if (!filters.includeUndrafted) return false
    }
    return true
  })
}

function useSeason(initialSeason, seasons) {
  const [season, setSeason]   = useState(initialSeason)
  const [players, setPlayers] = useState([])
  const [sel, setSel]         = useState(null)
  const [data, setData]       = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!seasons.length) return
    setPlayers([])
    setSel(null)
    setData(null)
    fetch(`/api/players?season=${season}`)
      .then(r => r.json())
      .then(list => {
        setPlayers(list)
        if (list.length > 0) setSel(list[0])
      })
  }, [season, seasons])

  return { season, setSeason, players, sel, setSel, data, setData, loading, setLoading }
}

export default function App() {
  const [seasons, setSeasons]       = useState([])
  const [filterOpen, setFilterOpen] = useState(false)
  const [filters, setFilters]       = useState(null)

  const a = useSeason('2025-26', seasons)
  const b = useSeason('2025-26', seasons)

  useEffect(() => {
    fetch('/api/seasons').then(r => r.json()).then(list => {
      setSeasons(list)
    })
  }, [])

  // Shared filter bounds from both player lists combined
  const defaults = useMemo(() => {
    const combined = [...a.players, ...b.players]
    return makeBounds(combined)
  }, [a.players, b.players])

  // Init filters when bounds first become available
  useEffect(() => {
    if (defaults && !filters) setFilters(defaults)
  }, [defaults])

  const filteredA = useMemo(() => applyFilters(a.players, filters, defaults), [a.players, filters, defaults])
  const filteredB = useMemo(() => applyFilters(b.players, filters, defaults), [b.players, filters, defaults])

  // Snap selection if filtered out
  useEffect(() => {
    if (filteredA.length && a.sel && !filteredA.find(p => p.id === a.sel.id)) a.setSel(filteredA[0])
  }, [filteredA])
  useEffect(() => {
    if (filteredB.length && b.sel && !filteredB.find(p => p.id === b.sel.id)) b.setSel(filteredB[0])
  }, [filteredB])

  // Set default second player to index 1
  useEffect(() => {
    if (b.players.length > 1 && b.sel?.id === b.players[0]?.id) b.setSel(b.players[1])
  }, [b.players])

  const fetchShots = useCallback((player, season, slot, setData, setLoading) => {
    if (!player) return
    setLoading(true)
    setData(null)
    fetch(`/api/shots/${player.id}?slot=${slot}&season=${season}`)
      .then(r => r.json())
      .then(d => setData({ ...d, name: player.name }))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => { fetchShots(a.sel, a.season, 'a', a.setData, a.setLoading) }, [a.sel, a.season])
  useEffect(() => { fetchShots(b.sel, b.season, 'b', b.setData, b.setLoading) }, [b.sel, b.season])

  return (
    <div className={styles.app}>
      <div className={styles.header}>
        <div className={styles.titleRow}>
          <h1 className={styles.title}>NBA Shot Chart</h1>
        </div>
        {filters && defaults && (
          <div className={styles.filterRow}>
            <FilterPanel
              open={filterOpen}
              onToggle={() => setFilterOpen(o => !o)}
              filters={filters}
              onChange={setFilters}
              defaults={defaults}
            />
          </div>
        )}
      </div>

      <div className={styles.selectors}>
        <div className={styles.selectorCol}>
          <SeasonSelect seasons={seasons} value={a.season} onChange={a.setSeason} />
          <PlayerSelect players={filteredA} selected={a.sel} onChange={a.setSel} label="Player 1" slot="a" />
        </div>
        <div className={styles.selectorCol}>
          <SeasonSelect seasons={seasons} value={b.season} onChange={b.setSeason} />
          <PlayerSelect players={filteredB} selected={b.sel} onChange={b.setSel} label="Player 2" slot="b" />
        </div>
      </div>

      <CompareCard dataA={a.data} dataB={b.data} loadingA={a.loading} loadingB={b.loading} seasonA={a.season} seasonB={b.season} />
    </div>
  )
}
