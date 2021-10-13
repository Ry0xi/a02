import Dexie from 'dexie'

// データベースの作成
const db = new Dexie('db')

// テーブルの作成
db.version(1).stores({
  user: 'id, name',
  task: '&id, title, detail, url, priority, next_display_date, display_times, consecutive_times, is_update, categories_id',
  category: '&id, name, color',
  offline_task: '&id, type',
  offline_category: '&id, type',
})

const testTasks = [
  {'id': '1001', 'name': 'タスク１', 'date': '2021-02-27', 'detail': '教材Aのp23~36を学んで、問題集p41~44を解く。', 'categories': ['0001','0002'], 'isDone': true},
  {'id': '1002', 'name': 'タスク２未完了', 'date': '2021-02-27', 'detail': '', 'categories': ['0001'], 'isDone': false},
  {'id': '1003', 'name': 'タスク３タスク３未完了', 'date': '2021-02-27', 'detail': '', 'categories': ['0001','0002'], 'isDone': false},
  {'id': '1004', 'name': 'タスク４タスク４タスク４タスク４', 'date': '2021-02-27', 'detail': '', 'categories': ['0001','0002', '0003'], 'isDone': true},
  {'id': '1005', 'name': 'タスク５タスク５タスク５タスク５タスク５タスク５タスク５未完了', 'date': '2021-02-27', 'detail': '', 'categories': ['0001','0002','0003'], 'isDone': false},
  {'id': '1006', 'name': 'タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６タスク６', 'date': '2021-02-27', 'detail': '', 'categories': ['0001','0002'], 'isDone': true},
];

const testCategoryData = [
  {'id': '0001', 'name': 'カテゴリ1カテゴリ1', 'color': '#FFC1C1'},
  {'id': '0002', 'name': 'カテゴリ2', 'color': '#FF9090'},
  {'id': '0003', 'name': 'カテゴリ3', 'color': '#D2BBF7'}
];

export default ({}, inject) => {
  inject('db', db);
  inject('testTasks', testTasks);
  inject('testCategoryData', testCategoryData);
}
