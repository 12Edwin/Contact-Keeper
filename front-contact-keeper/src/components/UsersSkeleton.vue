<template>
    <div class="skeleton-container">
        <div class="skeleton-row">
            <div class="skeleton-item skeleton-cell"></div>
            <div class="skeleton-item skeleton-cell"></div>
            <div class="skeleton-item skeleton-cell"></div>
        </div>
        <div class="skeleton-row">
            <div class="skeleton-item skeleton-cell"></div>
            <div class="skeleton-item skeleton-cell"></div>
            <div class="skeleton-item skeleton-cell"></div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'UsersSkeleton',
};
</script>

<style scoped>
.skeleton-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.skeleton-row {
    display: flex;
    gap: 1rem;
}

.skeleton-item {
    border-radius: 4px;
    background: #e0e0e0;
    /* Color de fondo del esqueleto */
    height: 1.5rem;
    /* Altura del esqueleto */
}

.skeleton-header {
    width: 100%;
    height: 2rem;
}

.skeleton-cell {
    flex: 1;
}
</style>