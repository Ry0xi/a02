export default function ({ redirect }) {
  if (!window.navigator.onLine) {
    redirect('/')
  }
}
