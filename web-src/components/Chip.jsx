const CLASS = {
  'High Risk': 'chip-high',
  Suspicious: 'chip-susp',
  Low: 'chip-low',
  'No Signal': 'chip-none',
  'Not Assessable': 'chip-na',
};

export const chipClass = (level) => CLASS[level] || 'chip-na';

export default function Chip({ level }) {
  return <span className={`chip ${chipClass(level)}`}>{level}</span>;
}
