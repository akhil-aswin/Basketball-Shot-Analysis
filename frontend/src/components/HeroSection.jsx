import { useState } from 'react'
import styles from './HeroSection.module.css'

function getInitials(name) {
  if (!name) return '??'
  return name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase()
}

function PlayerHero({ data, slot }) {
  const [logoFailed, setLogoFailed] = useState(false)
  const initials  = data ? getInitials(data.name) : '--'
  const team      = data?.team ?? ''
  const teamId    = data?.team_id ?? null
  const name      = data?.name ?? ''
  const archetype = data?.archetype ?? null
  const flip      = slot === 'b'

  const showLogo = teamId && !logoFailed

  return (
    <div className={`${styles.player} ${flip ? styles.flip : ''}`}>
      <div className={`${styles.avatar} ${styles[`avatar-${slot}`]} ${showLogo ? styles.avatarLogo : ''}`}>
        {showLogo ? (
          <img
            src={`https://cdn.nba.com/logos/nba/${teamId}/global/L/logo.svg`}
            className={styles.logoImg}
            alt={team}
            onError={() => setLogoFailed(true)}
          />
        ) : (
          initials
        )}
      </div>
      <div className={styles.info}>
        <p className={styles.playerName}>{name || ' '}</p>
        <div className={styles.meta}>
          {team && <span className={styles.teamName}>{team}</span>}
          {archetype && (
            <span className={`${styles.archetype} ${styles[`archetype-${slot}`]}`}>
              {archetype}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

export default function HeroSection({ dataA, dataB }) {
  return (
    <div className={styles.hero}>
      <PlayerHero data={dataA} slot="a" />
      <div className={styles.vsBadge}>VS</div>
      <PlayerHero data={dataB} slot="b" />
    </div>
  )
}
