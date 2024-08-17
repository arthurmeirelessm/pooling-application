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
    const s3 = new AWS.S3({
        endpoint: window.config.TRANSFER_ENDPOINT,
        useAccelerateEndpoint: true
    });

    const uploadKey = generateUUID();
    const partSize = 5 * 1024 * 1024; 
    const fileSize = fileStream.byteLength;
    const parts = new Array(Math.ceil(fileSize / partSize));
    console.log(fileStream.type)
    const contentType = fileStream.type || 'application/octet-stream'
    try {
        const createMulti = await s3.createMultipartUpload({
            Bucket: bucketName,
            Key: uploadKey,
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
                Key: uploadKey,
                PartNumber: partNumber,
                UploadId: uploadId
            }).promise().then(part => {
                parts[partNumber - 1] = { ETag: part.ETag, PartNumber: partNumber }; // Armazena a parte na posição correta
                console.log(`Parte ${partNumber} enviada com sucesso:`, part);
            }).catch(err => {
                console.error(`Erro ao enviar a parte ${partNumber}:`, err);
                throw err;
            });

            uploadPromises.push(uploadPromise);
        }

        // Espera todos os uploads de partes serem concluídos
        await Promise.all(uploadPromises);

        // Completa o upload multipart com as partes na ordem correta
        await s3.completeMultipartUpload({
            Bucket: bucketName,
            Key: uploadKey,
            MultipartUpload: { Parts: parts.filter(Boolean) }, // Remove elementos falsy se houver falhas
            UploadId: uploadId
        }).promise();
        
        await fetch('https://sis2f5ly6b.execute-api.us-east-1.amazonaws.com/dev/createstatus', {
            method: 'POST', 
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                "id": "43543543sdsdd"
            })
        });
        const statusDiv = document.getElementById("uploadStatus");
        statusDiv.className = "notification success";
        statusDiv.innerHTML = '<span class="icon">&#10003;</span><span class="message">Upload finalizado com sucesso!</span>';
        statusDiv.style.display = 'block';
       
    } catch (err) {
        const statusDiv = document.getElementById("uploadStatus");
        statusDiv.className = "notification error";
        statusDiv.innerHTML = '<span class="icon">&#10007;</span><span class="message">Erro ao finalizar o upload.</span>';
        statusDiv.style.display = 'block';
        console.error("Erro durante o upload:", err);
    }
}


// Função para lidar com o evento de upload do arquivo
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

// Função para ler o arquivo como ArrayBuffer
function getFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.onerror = (err) => reject(err);
        reader.readAsArrayBuffer(file);
    });
}

function generateUUID() {
    // Gera um número aleatório de 32 bits
    const crypto = window.crypto || window.msCrypto; // para compatibilidade com diferentes navegadores
    const array = new Uint8Array(16);
    crypto.getRandomValues(array);

    // Modifica os bytes conforme o padrão UUID v4
    array[6] = (array[6] & 0x0f) | 0x40; // define a versão (4)
    array[8] = (array[8] & 0x3f) | 0x80; // define o variante (10)

    // Converte os bytes para o formato UUID
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

