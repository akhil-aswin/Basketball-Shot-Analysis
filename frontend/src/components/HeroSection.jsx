import styles from './HeroSection.module.css'

function getInitials(name) {
  if (!name) return '??'
  return name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase()
}

function PlayerHero({ data, slot }) {
  const initials = data ? getInitials(data.name) : '--'
  const team     = data?.team ?? ''
  const name     = data?.name ?? ''
  const flip     = slot === 'b'

  return (
    <div className={`${styles.player} ${flip ? styles.flip : ''}`}>
      <div className={`${styles.avatar} ${styles[`avatar-${slot}`]}`}>
        {initials}
      </div>
      <div className={styles.info}>
        <p className={styles.playerName}>{name || ' '}</p>
        <p className={styles.teamName}>{team || ' '}</p>
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
