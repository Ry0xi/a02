import Dexie from 'dexie'

// データベースの作成
const db = new Dexie('db')

// テーブルの作成
db.version(1).stores({
  user: 'id, user_name',
  task: 'id, title, detail, url, priority, next_display_date, display_times, consecutive_times, is_update, category_id',
  category: 'id, category_name, color_code',
})

export default ({}, inject) => {
  inject('db', db)
}
