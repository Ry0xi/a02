import Dexie from 'dexie'

// データベースの作成
const db = new Dexie('db')

// テーブルの作成
db.version(1).stores({
  user: 'id, name',
  task: 'id, title, detail, url, priority, next_display_date, display_times, consecutive_times, is_update, categories_id',
  category: 'id, name, color',
  offline_task: 'id, type',
  offline_category: 'id, type',
})

export default ({}, inject) => {
  inject('db', db)
}
