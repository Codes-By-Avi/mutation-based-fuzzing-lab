import random
import subprocess
import os

# Original image
mainsource_image = "cross.jpg"

# Folder to keep all the mutated images
mutated_img_folder = "PA2_mutations"

# Recommended run parameters
mutation_attempts = 1500   # increase total runs to cover all bugs
byte_changes = 20         # number of bytes mutated per file (5–20)
timeout_seconds = 2       # timeout for jpeg2bmp execution

# Create folder if it doesn't exist
if not os.path.exists(mutated_img_folder):
    os.mkdir(mutated_img_folder)

# Keep track of bugs found
bug_counter = {}

# JPEG header length approximation for mutations
HEADER_LIMIT = 150

for trial_num in range(mutation_attempts):
    # Read the original image as bytes
    with open(mainsource_image, "rb") as f:
        byte_num = bytearray(f.read())

    # Decide how many bytes to mutate this time
    num_changes = random.randint(5, byte_changes)

    for _ in range(num_changes):
        # Header vs body mutation
        if random.random() < 0.5:
            idx = random.randint(0, min(HEADER_LIMIT - 1, len(byte_num) - 1))
        else:
            idx = random.randint(HEADER_LIMIT, len(byte_num) - 1)

        # Weighted mutation type selection
        mutation_type = random.choices(
            ["replace", "flip", "swap", "duplicate", "zero", "sequence_insert"],
            weights=[40, 20, 10, 10, 10, 10],
            k=1
        )[0]

        if mutation_type == "replace":
            byte_num[idx] = random.randint(0, 255)
        elif mutation_type == "flip":
            byte_num[idx] ^= 0xFF
        elif mutation_type == "swap":
            swap_idx = random.randint(0, len(byte_num) - 1)
            byte_num[idx], byte_num[swap_idx] = byte_num[swap_idx], byte_num[idx]
        elif mutation_type == "duplicate":
            byte_num.insert(idx, byte_num[idx])
        elif mutation_type == "zero":
            byte_num[idx] = 0
        elif mutation_type == "sequence_insert":
            seq_len = random.randint(2, 5)
            for _ in range(seq_len):
                byte_num.insert(idx, random.randint(0, 255))

    # Occasional SOF mutation to trigger color space bug (#3)
    if random.random() < 0.1:
        sof_idx = random.randint(10, 20)
        byte_num[sof_idx] = random.randint(0, 255)

    # Save mutated file
    mutated_file = f"{mutated_img_folder}/mutated_{trial_num}.jpg"
    with open(mutated_file, "wb") as f:
        f.write(byte_num)

    # Progress printout
    if (trial_num + 1) % 25 == 0:
        print(f"Progress: {trial_num + 1} / {mutation_attempts} runs completed")

    # Run jpeg2bmp to see if it crashes
    try:
        result = subprocess.run(
            ["./jpeg2bmp", mutated_file, "temp.bmp"],
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )

        if "CAP6135 Bug #" in result.stderr:
            bug_num = result.stderr.split("Bug #")[1].split(":")[0].strip()
            print(f"[Avionne Fuzzer] Bug {bug_num} found and saved as test-{bug_num}.jpg")
            bug_counter[bug_num] = bug_counter.get(bug_num, 0) + 1

            # Save proof file
            proof_file = f"test-{bug_num}.jpg"
            with open(proof_file, "wb") as pf:
                pf.write(byte_num)

    except subprocess.TimeoutExpired:
        print(f"[Avionne Fuzzer] Timeout on {mutated_file}")
    except Exception as e:
        print(f"[Avionne Fuzzer] Error on {mutated_file}: {e}")

# Summary
print("\n--- Bugs Found ---")
for bug, count in bug_counter.items():
    print(f"Bug {bug} triggered {count} times")

print(f"\nUnique bugs found: {len(bug_counter)}")
