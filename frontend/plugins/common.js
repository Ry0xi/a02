export default ({}, inject) => {
    const formatDate = (date) => {
        const dt = new Date(date)
        const year = dt.getFullYear()
        const month = dt.getMonth() + 1
        const day = dt.getDate()
        return `${year}年${month}月${day}日`
    }
    
    inject('formatDate', formatDate)
}