
export const formatTime = (time24) => {
    if (!time24) return 'N/A';
    if (time24 === '--:--') return '--:--';

    const [hours, minutes] = time24.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const hour12 = hour % 12 || 12;

    return `${hour12}:${minutes} ${ampm}`;
};