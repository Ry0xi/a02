export default async function ({ $db, $sync }) {
  if (navigator.onLine) {
    const responseCategory = await $db.offline_category.toArray()
    await $sync.category(responseCategory)

    const responseTask = await $db.offline_task.toArray()
    await $sync.task(responseTask)
  }
}
