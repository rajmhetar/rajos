/*
 * Minimal RajOS Test
 * Simple test to verify QEMU setup
 * Author: Raj Mhetar
 */

// Simple minimal test that should work
int main(void) {
    // Just loop forever - should at least start
    volatile int i = 0;
    while(1) {
        i++;
        if (i > 1000000) {
            i = 0;
        }
    }
    return 0;
}
