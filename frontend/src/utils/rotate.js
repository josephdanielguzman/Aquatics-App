export const executeRotation = (mutation, rotationId, time) => {
    /* Helper function to rotate lifeguard spots in a rotation */
    mutation.mutate({
        rotation_id: rotationId,
        payload: {
            time: time
        }
    });
};