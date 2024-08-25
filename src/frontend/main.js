function configureAWS() {
    AWS.config.update({
        region: 'us-east-1',
        credentials: new AWS.Credentials({
            accessKeyId: window.config.ACCESS_KEY,
            secretAccessKey: window.config.SECRET_KEY
        })
    });
}

async function uploadToS3Bucket(fileStream, bucketName, rawFileType) {
    console.log(rawFileType)
    const s3 = new AWS.S3({
        endpoint: window.config.TRANSFER_ENDPOINT,
        useAccelerateEndpoint: true
    });

    const uploadKey = generateUUID();
    const finalObjectKey = `${uploadKey}.${defineMediatoS3(rawFileType)}`
    const partSize = 5 * 1024 * 1024; 
    const fileSize = fileStream.byteLength;
    const parts = new Array(Math.ceil(fileSize / partSize));
    console.log(fileStream.type)
    const contentType = fileStream.type || 'application/octet-stream'
    try {
        const createMulti = await s3.createMultipartUpload({
            Bucket: bucketName,
            Key: finalObjectKey,
            ContentType: rawFileType
        }).promise();
        
        const uploadId = createMulti.UploadId;
        const uploadPromises = [];

        for (let start = 0; start < fileSize; start += partSize) {
            const end = Math.min(start + partSize, fileSize);
            const partNumber = Math.floor(start / partSize) + 1;
            const partStream = fileStream.slice(start, end);

            const uploadPromise = s3.uploadPart({
                Body: partStream,
                Bucket: bucketName,
                Key: finalObjectKey,
                PartNumber: partNumber,
                UploadId: uploadId
            }).promise().then(part => {
                parts[partNumber - 1] = { ETag: part.ETag, PartNumber: partNumber };
                console.log(`Parte ${partNumber} enviada com sucesso:`, part);
            }).catch(err => {
                console.error(`Erro ao enviar a parte ${partNumber}:`, err);
                throw err;
            });

            uploadPromises.push(uploadPromise);
        }

        await Promise.all(uploadPromises);

        console.log(finalObjectKey)

        await s3.completeMultipartUpload({
            Bucket: bucketName,
            Key: finalObjectKey,
            MultipartUpload: { Parts: parts.filter(Boolean) }, 
            UploadId: uploadId
        }).promise();

        const statusDiv = document.getElementById("uploadStatus");
        statusDiv.className = "notification success";
        statusDiv.innerHTML = '<span class="icon">&#10003;</span><span class="message">Upload finalizado com sucesso!</span>';
        statusDiv.style.display = 'block';
        const data = {
            "id": finalObjectKey
        }
        fetch(window.config.CREATE_STATUS_ENDPOINT, {
            method: "POST", 
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data) 
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json(); 
        })
        .then(responseData => {
            console.log("Resposta do servidor:", responseData);
        })
        .catch(error => {
            console.error("Erro ao chamar o endpoint:", error);
        });

    } catch (err) {
        const statusDiv = document.getElementById("uploadStatus");
        statusDiv.className = "notification error";
        statusDiv.innerHTML = '<span class="icon">&#10007;</span><span class="message">Erro ao finalizar o upload.</span>';
        statusDiv.style.display = 'block';
        console.error("Erro durante o upload:", err);
    }
}


async function uploadMedia() {
    try {
        const fileInput = document.getElementById("fileToUpload");
        if (!fileInput.files[0]) {
            throw new Error("Nenhum arquivo selecionado.");
        }
        
        const rawFileType = fileInput.files[0].type
        const fileStream = await getFile(fileInput.files[0]);
        const bucketName = 'pooling-application-bucket';

        await uploadToS3Bucket(fileStream, bucketName, rawFileType);
    } catch (err) {
        console.error("Erro no upload:", err);
        document.getElementById("uploadStatus").textContent = "Erro no upload.";
    }
}

function getFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (err) => reject(err);
        reader.readAsArrayBuffer(file);
    });
}

function generateUUID() {
    const crypto = window.crypto || window.msCrypto; 
    const array = new Uint8Array(16);
    crypto.getRandomValues(array);

    array[6] = (array[6] & 0x0f) | 0x40; 
    array[8] = (array[8] & 0x3f) | 0x80; 

    const hexArray = Array.from(array, byte => byte.toString(16).padStart(2, '0'));
    return [
        hexArray.slice(0, 4).join(''),
        hexArray.slice(4, 6).join(''),
        hexArray.slice(6, 8).join(''),
        hexArray.slice(8, 10).join(''),
        hexArray.slice(10).join('')
    ].join('-');

}

document.addEventListener("DOMContentLoaded", () => {
    configureAWS();
});


function defineMediatoS3(mediaType) {
    const mediaFormat = mediaType.split('/')[1];
    return mediaFormat;
}

